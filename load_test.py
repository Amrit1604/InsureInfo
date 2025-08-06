"""
🔥 LOAD TESTING SCRIPT
=====================
Tests API performance under concurrent load
Simulates multiple users hitting the API simultaneously

Usage:
    python load_test.py [concurrent_users] [requests_per_user]

Examples:
    python load_test.py 5 3    # 5 users, 3 requests each
    python load_test.py 10 2   # 10 users, 2 requests each
"""

import requests
import time
import json
import threading
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
import statistics

init(autoreset=True)

class LoadTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.lock = threading.Lock()

    def single_request(self, user_id, request_id, question):
        """Make a single API request"""
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
                timeout=60
            )

            response_time = time.time() - start_time

            with self.lock:
                result = {
                    'user_id': user_id,
                    'request_id': request_id,
                    'question': question,
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'success': response.status_code == 200,
                    'timestamp': time.time()
                }

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('answers') and len(data['answers']) > 0:
                            answer = data['answers'][0]['answer']
                            result['answer_length'] = len(answer)
                            result['has_answer'] = True

                            # Check for generic responses
                            generic_phrases = [
                                "sorry, there was an error",
                                "unable to process",
                                "contact customer service"
                            ]
                            result['is_generic'] = any(phrase in answer.lower() for phrase in generic_phrases)
                        else:
                            result['has_answer'] = False
                    except:
                        result['has_answer'] = False

                self.results.append(result)

            return result

        except Exception as e:
            response_time = time.time() - start_time

            with self.lock:
                result = {
                    'user_id': user_id,
                    'request_id': request_id,
                    'question': question,
                    'response_time': response_time,
                    'success': False,
                    'error': str(e),
                    'timestamp': time.time()
                }
                self.results.append(result)

            return result

    def user_simulation(self, user_id, requests_per_user, questions):
        """Simulate a single user making multiple requests"""
        print(f"{Fore.YELLOW}👤 User {user_id} starting {requests_per_user} requests...")

        for req_id in range(requests_per_user):
            question = questions[req_id % len(questions)]  # Cycle through questions
            result = self.single_request(user_id, req_id, question)

            status = "✅" if result['success'] else "❌"
            print(f"   {status} User {user_id} Req {req_id+1}: {result['response_time']:.2f}s")

            # Small delay between requests from same user
            time.sleep(0.1)

    def run_load_test(self, concurrent_users=5, requests_per_user=3):
        """Run the load test"""
        print(f"{Fore.CYAN}🔥 Load Test Configuration:")
        print(f"   Concurrent Users: {concurrent_users}")
        print(f"   Requests per User: {requests_per_user}")
        print(f"   Total Requests: {concurrent_users * requests_per_user}")
        print("=" * 50)

        # Test questions pool
        questions = [
            "I broke my arm, am I covered?",
            "What is the grace period for premium payment?",
            "Emergency heart attack needs immediate treatment",
            "Diabetic patient requires surgery for complications",
            "Pregnancy emergency requiring C-section delivery",
            "Does this policy cover dental treatments?",
            "What is the maximum coverage amount available?",
            "Pre-existing disease waiting period query",
            "Treatment needed in different state while traveling",
            "Cancer treatment coverage with rider benefits"
        ]

        # Clear previous results
        self.results = []

        # Start load test
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # Submit all user simulations
            futures = []
            for user_id in range(concurrent_users):
                future = executor.submit(self.user_simulation, user_id, requests_per_user, questions)
                futures.append(future)

            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"{Fore.RED}User simulation error: {e}")

        total_time = time.time() - start_time

        # Analyze results
        self.analyze_results(total_time, concurrent_users, requests_per_user)

    def analyze_results(self, total_time, concurrent_users, requests_per_user):
        """Analyze and display load test results"""
        print(f"\n{Fore.GREEN}📊 Load Test Results:")
        print("=" * 40)

        if not self.results:
            print(f"{Fore.RED}❌ No results to analyze!")
            return

        # Basic stats
        total_requests = len(self.results)
        successful_requests = [r for r in self.results if r['success']]
        failed_requests = [r for r in self.results if not r['success']]

        print(f"📈 Overall Performance:")
        print(f"   Total Requests: {total_requests}")
        print(f"   Successful: {len(successful_requests)} ({len(successful_requests)/total_requests*100:.1f}%)")
        print(f"   Failed: {len(failed_requests)} ({len(failed_requests)/total_requests*100:.1f}%)")
        print(f"   Total Test Duration: {total_time:.2f}s")

        if successful_requests:
            # Response time analysis
            response_times = [r['response_time'] for r in successful_requests]

            print(f"\n⏱️  Response Time Analysis:")
            print(f"   Average: {statistics.mean(response_times):.2f}s")
            print(f"   Median: {statistics.median(response_times):.2f}s")
            print(f"   Min: {min(response_times):.2f}s")
            print(f"   Max: {max(response_times):.2f}s")

            if len(response_times) > 1:
                print(f"   Std Dev: {statistics.stdev(response_times):.2f}s")

            # Throughput
            requests_per_second = total_requests / total_time
            successful_per_second = len(successful_requests) / total_time

            print(f"\n🚀 Throughput:")
            print(f"   Total RPS: {requests_per_second:.2f}")
            print(f"   Successful RPS: {successful_per_second:.2f}")

            # Quality analysis
            quality_responses = [r for r in successful_requests if r.get('has_answer') and not r.get('is_generic', True)]

            print(f"\n🎯 Response Quality:")
            print(f"   Quality Responses: {len(quality_responses)}/{len(successful_requests)} ({len(quality_responses)/len(successful_requests)*100:.1f}%)")

            # Concurrency analysis
            print(f"\n🔀 Concurrency Performance:")
            user_performance = {}
            for result in successful_requests:
                user_id = result['user_id']
                if user_id not in user_performance:
                    user_performance[user_id] = []
                user_performance[user_id].append(result['response_time'])

            for user_id, times in user_performance.items():
                avg_time = statistics.mean(times)
                print(f"   User {user_id}: {len(times)} requests, avg {avg_time:.2f}s")

            # Performance grade
            avg_response_time = statistics.mean(response_times)
            success_rate = len(successful_requests) / total_requests
            quality_rate = len(quality_responses) / len(successful_requests) if successful_requests else 0

            if avg_response_time < 5 and success_rate >= 0.95 and quality_rate >= 0.8:
                grade = "🏆 A+ (Excellent)"
            elif avg_response_time < 10 and success_rate >= 0.9 and quality_rate >= 0.6:
                grade = "🥇 A (Good)"
            elif avg_response_time < 20 and success_rate >= 0.8 and quality_rate >= 0.4:
                grade = "🥈 B (Fair)"
            else:
                grade = "🥉 C (Needs Improvement)"

            print(f"\n📈 Overall Load Test Grade: {grade}")

        # Error analysis
        if failed_requests:
            print(f"\n❌ Error Analysis:")
            error_types = {}
            for req in failed_requests:
                error = req.get('error', 'Unknown')
                error_types[error] = error_types.get(error, 0) + 1

            for error, count in error_types.items():
                print(f"   {error}: {count} occurrences")

def main():
    """Main function"""
    # Parse command line arguments
    concurrent_users = 5
    requests_per_user = 3

    if len(sys.argv) >= 2:
        try:
            concurrent_users = int(sys.argv[1])
        except ValueError:
            print(f"{Fore.RED}Invalid concurrent_users value. Using default: 5")

    if len(sys.argv) >= 3:
        try:
            requests_per_user = int(sys.argv[2])
        except ValueError:
            print(f"{Fore.RED}Invalid requests_per_user value. Using default: 3")

    print(f"{Fore.GREEN}🚀 Starting Load Test...")

    # Check if API is running
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

    # Run load test
    tester = LoadTester()
    tester.run_load_test(concurrent_users, requests_per_user)

    print(f"\n{Fore.GREEN}🎉 Load test completed!")

if __name__ == "__main__":
    main()
