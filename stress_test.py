"""
💥 STRESS TESTING SCRIPT
=======================
Pushes API to its limits with extreme load
Tests system breaking points and recovery

Usage:
    python stress_test.py [test_type]

Test Types:
    1. ramp_up     - Gradually increase load
    2. spike       - Sudden traffic spike
    3. sustained   - High sustained load
    4. burst       - Burst traffic patterns

Examples:
    python stress_test.py ramp_up
    python stress_test.py spike
"""

import requests
import time
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
import statistics
from datetime import datetime

init(autoreset=True)

class StressTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.lock = threading.Lock()
        self.active_requests = 0
        self.peak_concurrent = 0

    def single_stress_request(self, test_id, user_id, question):
        """Make a single stress test request"""
        with self.lock:
            self.active_requests += 1
            if self.active_requests > self.peak_concurrent:
                self.peak_concurrent = self.active_requests

        start_time = time.time()

        try:
            payload = {
                "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
                "questions": [question]
            }

            response = requests.post(
                f"{self.base_url}/hackrx/run",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120  # Extended timeout for stress test
            )

            response_time = time.time() - start_time

            result = {
                'test_id': test_id,
                'user_id': user_id,
                'timestamp': time.time(),
                'response_time': response_time,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'concurrent_active': self.active_requests
            }

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('answers') and len(data['answers']) > 0:
                        answer = data['answers'][0]['answer']
                        result['answer_length'] = len(answer)
                        result['has_quality_answer'] = len(answer) > 100 and "sorry" not in answer.lower()
                    else:
                        result['has_quality_answer'] = False
                except:
                    result['has_quality_answer'] = False

            with self.lock:
                self.results.append(result)
                self.active_requests -= 1

            return result

        except Exception as e:
            response_time = time.time() - start_time

            result = {
                'test_id': test_id,
                'user_id': user_id,
                'timestamp': time.time(),
                'response_time': response_time,
                'success': False,
                'error': str(e),
                'concurrent_active': self.active_requests
            }

            with self.lock:
                self.results.append(result)
                self.active_requests -= 1

            return result

    def ramp_up_test(self):
        """Gradually increase load to find breaking point"""
        print(f"{Fore.CYAN}🚀 Ramp-Up Stress Test")
        print("=" * 40)

        questions = [
            "Emergency heart surgery coverage needed immediately",
            "Pregnancy complications require emergency C-section",
            "Diabetic patient needs urgent insulin treatment",
            "Broken bone from accident needs immediate surgery",
            "Cancer patient requires chemotherapy coverage",
            "Mental health crisis requires immediate treatment",
            "Kidney failure patient needs dialysis coverage",
            "Stroke patient requires emergency brain surgery",
            "Severe burns require specialized treatment coverage",
            "Spinal injury from accident needs surgery"
        ]

        stages = [1, 2, 5, 10, 20, 30, 50, 75, 100]

        for stage, concurrent_users in enumerate(stages):
            print(f"\n📈 Stage {stage + 1}: {concurrent_users} concurrent users")

            stage_start = time.time()
            stage_results = []

            with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                futures = []

                for user_id in range(concurrent_users):
                    question = questions[user_id % len(questions)]
                    future = executor.submit(
                        self.single_stress_request,
                        f"ramp_{stage}",
                        user_id,
                        question
                    )
                    futures.append(future)

                # Collect results
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        stage_results.append(result)
                    except Exception as e:
                        print(f"   ❌ Request failed: {e}")

            stage_duration = time.time() - stage_start
            successful = [r for r in stage_results if r['success']]

            success_rate = len(successful) / len(stage_results) if stage_results else 0
            avg_response_time = statistics.mean([r['response_time'] for r in successful]) if successful else 0

            print(f"   Results: {len(successful)}/{len(stage_results)} success ({success_rate*100:.1f}%)")
            print(f"   Avg Response Time: {avg_response_time:.2f}s")
            print(f"   Stage Duration: {stage_duration:.2f}s")

            # Check if system is breaking
            if success_rate < 0.5:
                print(f"   {Fore.RED}🚨 System breaking point reached!")
                break

            # Brief recovery time between stages
            time.sleep(2)

        print(f"\n{Fore.GREEN}✅ Ramp-up test completed")

    def spike_test(self):
        """Sudden traffic spike test"""
        print(f"{Fore.CYAN}⚡ Traffic Spike Test")
        print("=" * 40)

        questions = [
            "EMERGENCY: Heart attack patient needs immediate coverage",
            "URGENT: Pregnancy emergency requiring surgery",
            "CRITICAL: Diabetic coma requires emergency treatment",
            "EMERGENCY: Severe accident victim needs surgery",
            "URGENT: Child with appendicitis needs operation"
        ]

        # Baseline load
        print("📊 Phase 1: Baseline load (5 users)")
        baseline_start = time.time()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(5):
                question = questions[i % len(questions)]
                future = executor.submit(self.single_stress_request, "baseline", i, question)
                futures.append(future)

            for future in as_completed(futures):
                future.result()

        baseline_duration = time.time() - baseline_start
        print(f"   Baseline completed in {baseline_duration:.2f}s")

        # Wait period
        print("⏳ Phase 2: Normal period (2 second pause)")
        time.sleep(2)

        # Sudden spike
        print("💥 Phase 3: TRAFFIC SPIKE (50 users suddenly)")
        spike_start = time.time()

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for i in range(50):
                question = questions[i % len(questions)]
                future = executor.submit(self.single_stress_request, "spike", i, question)
                futures.append(future)

            # Collect results with progress
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    if completed % 10 == 0:
                        print(f"   {completed}/50 requests completed...")
                except Exception as e:
                    print(f"   ❌ Request failed: {e}")

        spike_duration = time.time() - spike_start
        print(f"   Spike completed in {spike_duration:.2f}s")

        print(f"\n{Fore.GREEN}✅ Spike test completed")

    def sustained_test(self):
        """High sustained load test"""
        print(f"{Fore.CYAN}🔥 Sustained Load Test")
        print("=" * 40)

        questions = [
            "Ongoing diabetes treatment coverage questions",
            "Regular pregnancy checkup coverage inquiry",
            "Routine heart medication coverage check",
            "Monthly therapy session coverage verification",
            "Annual health checkup coverage details",
            "Prescription drug coverage for chronic condition",
            "Physical therapy coverage for injury recovery",
            "Specialist consultation coverage verification",
            "Diagnostic test coverage for health monitoring",
            "Preventive care coverage inquiry"
        ]

        concurrent_users = 25
        test_duration = 60  # seconds

        print(f"🎯 Test Parameters:")
        print(f"   Concurrent Users: {concurrent_users}")
        print(f"   Duration: {test_duration} seconds")
        print(f"   Expected Requests: ~{concurrent_users * test_duration / 5}")

        start_time = time.time()
        request_counter = 0

        def sustained_worker(worker_id):
            """Worker function for sustained load"""
            nonlocal request_counter

            while time.time() - start_time < test_duration:
                question = questions[request_counter % len(questions)]

                try:
                    result = self.single_stress_request("sustained", worker_id, question)

                    with self.lock:
                        request_counter += 1
                        if request_counter % 20 == 0:
                            elapsed = time.time() - start_time
                            print(f"   {request_counter} requests in {elapsed:.1f}s...")

                    # Small delay to simulate realistic usage
                    time.sleep(0.2)

                except Exception as e:
                    print(f"   ❌ Worker {worker_id} error: {e}")

        # Start sustained load
        print(f"\n🚀 Starting sustained load...")

        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            for worker_id in range(concurrent_users):
                future = executor.submit(sustained_worker, worker_id)
                futures.append(future)

            # Wait for all workers to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"   ❌ Worker error: {e}")

        total_duration = time.time() - start_time
        print(f"\n✅ Sustained test completed in {total_duration:.2f}s")

    def burst_test(self):
        """Burst traffic pattern test"""
        print(f"{Fore.CYAN}💥 Burst Pattern Test")
        print("=" * 40)

        questions = [
            "Quick coverage verification needed",
            "Fast claim status check",
            "Rapid eligibility confirmation",
            "Immediate coverage amount check",
            "Quick policy benefit verification"
        ]

        # Multiple burst cycles
        for burst_cycle in range(5):
            print(f"\n💥 Burst Cycle {burst_cycle + 1}/5")

            # High intensity burst
            burst_start = time.time()

            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = []
                for i in range(20):
                    question = questions[i % len(questions)]
                    future = executor.submit(
                        self.single_stress_request,
                        f"burst_{burst_cycle}",
                        i,
                        question
                    )
                    futures.append(future)

                completed = 0
                for future in as_completed(futures):
                    try:
                        future.result()
                        completed += 1
                    except Exception as e:
                        print(f"   ❌ Burst request failed: {e}")

            burst_duration = time.time() - burst_start
            print(f"   Burst completed: {completed}/20 in {burst_duration:.2f}s")

            # Cool down period
            print("   💤 Cool down period (3s)")
            time.sleep(3)

        print(f"\n{Fore.GREEN}✅ Burst test completed")

    def analyze_stress_results(self):
        """Analyze stress test results"""
        if not self.results:
            print(f"{Fore.RED}❌ No results to analyze!")
            return

        print(f"\n{Fore.GREEN}📊 STRESS TEST ANALYSIS")
        print("=" * 50)

        # Overall statistics
        total_requests = len(self.results)
        successful_requests = [r for r in self.results if r['success']]
        failed_requests = [r for r in self.results if not r['success']]

        print(f"📈 Overall Performance:")
        print(f"   Total Requests: {total_requests}")
        print(f"   Successful: {len(successful_requests)} ({len(successful_requests)/total_requests*100:.1f}%)")
        print(f"   Failed: {len(failed_requests)} ({len(failed_requests)/total_requests*100:.1f}%)")
        print(f"   Peak Concurrent Requests: {self.peak_concurrent}")

        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]

            print(f"\n⏱️  Response Time Analysis:")
            print(f"   Average: {statistics.mean(response_times):.2f}s")
            print(f"   Median: {statistics.median(response_times):.2f}s")
            print(f"   Min: {min(response_times):.2f}s")
            print(f"   Max: {max(response_times):.2f}s")
            print(f"   95th Percentile: {statistics.quantiles(response_times, n=20)[18]:.2f}s")

            # Performance under load
            high_load_results = [r for r in successful_requests if r.get('concurrent_active', 0) > 10]
            if high_load_results:
                high_load_times = [r['response_time'] for r in high_load_results]
                print(f"\n🔥 High Load Performance (>10 concurrent):")
                print(f"   Requests under load: {len(high_load_results)}")
                print(f"   Avg response time: {statistics.mean(high_load_times):.2f}s")

        # Quality analysis
        quality_responses = [r for r in successful_requests if r.get('has_quality_answer', False)]
        print(f"\n🎯 Quality Under Stress:")
        print(f"   Quality responses: {len(quality_responses)}/{len(successful_requests)} ({len(quality_responses)/len(successful_requests)*100:.1f}%)")

        # Error analysis
        if failed_requests:
            print(f"\n❌ Error Analysis:")
            error_types = {}
            for req in failed_requests:
                error = req.get('error', 'HTTP Error')
                if 'timeout' in error.lower():
                    error_type = 'Timeout'
                elif 'connection' in error.lower():
                    error_type = 'Connection Error'
                else:
                    error_type = 'Other Error'

                error_types[error_type] = error_types.get(error_type, 0) + 1

            for error_type, count in error_types.items():
                print(f"   {error_type}: {count} occurrences")

        # System resilience grade
        success_rate = len(successful_requests) / total_requests
        avg_response_time = statistics.mean([r['response_time'] for r in successful_requests]) if successful_requests else float('inf')

        if success_rate >= 0.95 and avg_response_time < 10:
            grade = f"{Fore.GREEN}🏆 A+ (Excellent Resilience)"
        elif success_rate >= 0.9 and avg_response_time < 15:
            grade = f"{Fore.GREEN}🥇 A (Good Resilience)"
        elif success_rate >= 0.8 and avg_response_time < 25:
            grade = f"{Fore.YELLOW}🥈 B (Fair Resilience)"
        else:
            grade = f"{Fore.RED}🥉 C (Poor Resilience)"

        print(f"\n📊 System Resilience Grade: {grade}")

        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stress_test_results_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📄 Detailed results saved: {filename}")

def main():
    """Main function"""
    test_type = "ramp_up"

    if len(sys.argv) >= 2:
        test_type = sys.argv[1].lower()

    valid_tests = ["ramp_up", "spike", "sustained", "burst"]
    if test_type not in valid_tests:
        print(f"{Fore.RED}❌ Invalid test type: {test_type}")
        print(f"{Fore.YELLOW}Valid options: {', '.join(valid_tests)}")
        return

    print(f"{Fore.GREEN}🔥 Starting Stress Test: {test_type.upper()}")

    # Check if API is running
    tester = StressTester()

    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print(f"{Fore.RED}❌ API not responding")
            return
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}❌ Cannot connect to API")
        print(f"{Fore.YELLOW}💡 Please start the API server: python api_server.py")
        return

    print(f"{Fore.GREEN}✅ API is running")

    # Run selected stress test
    if test_type == "ramp_up":
        tester.ramp_up_test()
    elif test_type == "spike":
        tester.spike_test()
    elif test_type == "sustained":
        tester.sustained_test()
    elif test_type == "burst":
        tester.burst_test()

    # Analyze results
    tester.analyze_stress_results()

    print(f"\n{Fore.GREEN}🎉 Stress test completed!")

if __name__ == "__main__":
    main()
