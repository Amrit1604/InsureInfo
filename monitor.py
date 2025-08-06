"""
📊 REAL-TIME API MONITOR
=======================
Monitors API performance in real-time with live metrics
Tracks response times, success rates, and system health

Usage:
    python monitor.py [interval_seconds] [test_duration_minutes]

Examples:
    python monitor.py 5 10     # Test every 5 seconds for 10 minutes
    python monitor.py 2 30     # Test every 2 seconds for 30 minutes
"""

import requests
import time
import json
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import statistics
import threading

init(autoreset=True)

class APIMonitor:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.metrics = []
        self.is_running = False
        self.start_time = None

    def health_check(self):
        """Perform health check"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def performance_test(self):
        """Single performance test request"""
        test_questions = [
            "I broke my arm skiing, am I covered for treatment?",
            "Emergency heart attack, need immediate surgery coverage",
            "Pregnancy complications requiring C-section",
            "Diabetic patient needs specialized treatment",
            "What is the maximum coverage for dental work?"
        ]

        question = test_questions[len(self.metrics) % len(test_questions)]

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

            metric = {
                'timestamp': datetime.now(),
                'response_time': response_time,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'question': question
            }

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('answers') and len(data['answers']) > 0:
                        answer = data['answers'][0]['answer']
                        metric['answer_length'] = len(answer)
                        metric['has_answer'] = True

                        # Check for generic responses
                        generic_phrases = [
                            "sorry, there was an error",
                            "unable to process",
                            "contact customer service"
                        ]
                        metric['is_generic'] = any(phrase in answer.lower() for phrase in generic_phrases)
                    else:
                        metric['has_answer'] = False
                        metric['is_generic'] = True
                except:
                    metric['has_answer'] = False
                    metric['is_generic'] = True

            return metric

        except Exception as e:
            response_time = time.time() - start_time
            return {
                'timestamp': datetime.now(),
                'response_time': response_time,
                'success': False,
                'error': str(e),
                'question': question
            }

    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_metrics(self):
        """Display live metrics"""
        self.clear_screen()

        print(f"{Fore.CYAN}🔴 LIVE API MONITORING")
        print("=" * 60)

        if not self.metrics:
            print(f"{Fore.YELLOW}⏳ Waiting for first test result...")
            return

        # Recent metrics (last 10)
        recent_metrics = self.metrics[-10:]
        successful_recent = [m for m in recent_metrics if m['success']]

        # Overall metrics
        total_requests = len(self.metrics)
        total_successful = len([m for m in self.metrics if m['success']])
        total_failed = total_requests - total_successful

        # Current status
        last_metric = self.metrics[-1]
        status_icon = "🟢" if last_metric['success'] else "🔴"

        print(f"{status_icon} Current Status: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Last Response Time: {last_metric['response_time']:.2f}s")
        print(f"   Last Status: {'✅ Success' if last_metric['success'] else '❌ Failed'}")

        # Overall statistics
        print(f"\n📊 Overall Statistics:")
        print(f"   Total Requests: {total_requests}")
        print(f"   Success Rate: {total_successful}/{total_requests} ({total_successful/total_requests*100:.1f}%)")
        print(f"   Failed Requests: {total_failed}")

        if self.start_time:
            uptime = datetime.now() - self.start_time
            print(f"   Monitoring Duration: {str(uptime).split('.')[0]}")

        # Response time analysis
        if successful_recent:
            response_times = [m['response_time'] for m in successful_recent]

            print(f"\n⏱️  Response Time (Last 10 successful):")
            print(f"   Average: {statistics.mean(response_times):.2f}s")
            print(f"   Min: {min(response_times):.2f}s")
            print(f"   Max: {max(response_times):.2f}s")

            if len(response_times) > 1:
                print(f"   Std Dev: {statistics.stdev(response_times):.2f}s")

        # Quality metrics
        quality_responses = [m for m in successful_recent if m.get('has_answer') and not m.get('is_generic', True)]
        if successful_recent:
            quality_rate = len(quality_responses) / len(successful_recent) * 100
            print(f"\n🎯 Quality Metrics (Last 10):")
            print(f"   Quality Responses: {len(quality_responses)}/{len(successful_recent)} ({quality_rate:.1f}%)")

        # Recent activity timeline
        print(f"\n📈 Recent Activity:")
        for i, metric in enumerate(recent_metrics[-5:]):  # Last 5
            timestamp = metric['timestamp'].strftime('%H:%M:%S')
            status = "✅" if metric['success'] else "❌"
            response_time = metric['response_time']

            print(f"   {timestamp} {status} {response_time:.2f}s")

        # Performance trend
        if len(self.metrics) >= 10:
            old_batch = self.metrics[-20:-10] if len(self.metrics) >= 20 else self.metrics[:-10]
            new_batch = self.metrics[-10:]

            old_avg = statistics.mean([m['response_time'] for m in old_batch if m['success']])
            new_avg = statistics.mean([m['response_time'] for m in new_batch if m['success']])

            trend = "📈" if new_avg > old_avg else "📉"
            change = ((new_avg - old_avg) / old_avg) * 100

            print(f"\n{trend} Performance Trend:")
            print(f"   Response time change: {change:+.1f}%")

        # Health indicators
        print(f"\n🏥 Health Indicators:")

        # Success rate indicator
        success_rate = total_successful / total_requests if total_requests > 0 else 0
        if success_rate >= 0.95:
            health_status = f"{Fore.GREEN}🟢 Excellent"
        elif success_rate >= 0.9:
            health_status = f"{Fore.YELLOW}🟡 Good"
        elif success_rate >= 0.8:
            health_status = f"{Fore.YELLOW}🟠 Fair"
        else:
            health_status = f"{Fore.RED}🔴 Poor"

        print(f"   System Health: {health_status}")

        # Response time indicator
        if successful_recent:
            avg_response = statistics.mean([m['response_time'] for m in successful_recent])
            if avg_response < 5:
                speed_status = f"{Fore.GREEN}🚀 Fast"
            elif avg_response < 10:
                speed_status = f"{Fore.YELLOW}⚡ Moderate"
            elif avg_response < 20:
                speed_status = f"{Fore.YELLOW}🐌 Slow"
            else:
                speed_status = f"{Fore.RED}🐢 Very Slow"

            print(f"   Response Speed: {speed_status}")

        print(f"\n{Fore.CYAN}Press Ctrl+C to stop monitoring...")

    def monitor(self, interval=5, duration_minutes=None):
        """Start monitoring"""
        self.is_running = True
        self.start_time = datetime.now()
        end_time = self.start_time + timedelta(minutes=duration_minutes) if duration_minutes else None

        print(f"{Fore.GREEN}🚀 Starting API monitoring...")
        print(f"   Interval: {interval} seconds")
        if duration_minutes:
            print(f"   Duration: {duration_minutes} minutes")
        else:
            print(f"   Duration: Continuous (Ctrl+C to stop)")

        try:
            while self.is_running:
                # Check if we should stop
                if end_time and datetime.now() >= end_time:
                    break

                # Perform test
                metric = self.performance_test()
                self.metrics.append(metric)

                # Display metrics
                self.display_metrics()

                # Wait for next interval
                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️  Monitoring stopped by user")

        self.is_running = False
        self.generate_report()

    def generate_report(self):
        """Generate final monitoring report"""
        if not self.metrics:
            return

        print(f"\n{Fore.GREEN}📊 MONITORING REPORT")
        print("=" * 40)

        # Save results to file
        report_data = {
            'monitoring_session': {
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration': str(datetime.now() - self.start_time),
                'total_requests': len(self.metrics)
            },
            'metrics': []
        }

        for metric in self.metrics:
            metric_copy = metric.copy()
            metric_copy['timestamp'] = metric_copy['timestamp'].isoformat()
            report_data['metrics'].append(metric_copy)

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"monitoring_report_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📄 Report saved: {filename}")

        # Summary statistics
        successful_metrics = [m for m in self.metrics if m['success']]

        if successful_metrics:
            response_times = [m['response_time'] for m in successful_metrics]

            print(f"\n📈 Summary Statistics:")
            print(f"   Success Rate: {len(successful_metrics)}/{len(self.metrics)} ({len(successful_metrics)/len(self.metrics)*100:.1f}%)")
            print(f"   Avg Response Time: {statistics.mean(response_times):.2f}s")
            print(f"   Min Response Time: {min(response_times):.2f}s")
            print(f"   Max Response Time: {max(response_times):.2f}s")

def main():
    """Main function"""
    # Parse command line arguments
    interval = 5  # seconds
    duration = None  # minutes

    if len(sys.argv) >= 2:
        try:
            interval = int(sys.argv[1])
            if interval < 1:
                interval = 1
        except ValueError:
            print(f"{Fore.RED}Invalid interval value. Using default: 5 seconds")

    if len(sys.argv) >= 3:
        try:
            duration = int(sys.argv[2])
            if duration < 1:
                duration = None
        except ValueError:
            print(f"{Fore.RED}Invalid duration value. Running continuously...")

    # Check if API is running
    monitor = APIMonitor()

    if not monitor.health_check():
        print(f"{Fore.RED}❌ Cannot connect to API")
        print(f"{Fore.YELLOW}💡 Please start the API server: python api_server.py")
        return

    print(f"{Fore.GREEN}✅ API is running")

    # Start monitoring
    monitor.monitor(interval, duration)

if __name__ == "__main__":
    main()
