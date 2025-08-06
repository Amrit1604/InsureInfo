"""
⚡ QUICK BENCHMARK TEST
=====================
Fast benchmark test for immediate feedback
Focuses on speed and basic functionality

Usage:
    python quick_benchmark.py
"""

import requests
import time
import json
from colorama import init, Fore, Style

init(autoreset=True)

def quick_benchmark():
    """Run a quick 5-question benchmark test"""
    base_url = "http://localhost:8000"

    # Quick test questions
    test_questions = [
        "I broke my arm, am I covered?",
        "What is the grace period for premium payment?",
        "Emergency heart attack, need immediate approval",
        "Diabetic patient needs surgery, pre-existing condition concern",
        "Pregnancy complications requiring emergency C-section"
    ]

    print(f"{Fore.CYAN}⚡ Quick Benchmark Test - 5 Questions")
    print("=" * 40)

    total_start = time.time()
    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"{Fore.YELLOW}{i}. {question[:50]}...")

        start_time = time.time()

        try:
            payload = {
                "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
                "questions": [question]
            }

            response = requests.post(
                f"{base_url}/hackrx/run",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get('answers') and len(data['answers']) > 0:
                    answer = data['answers'][0]['answer']

                    # Quick quality check
                    is_generic = any(phrase in answer.lower() for phrase in [
                        "sorry, there was an error",
                        "unable to process",
                        "contact customer service"
                    ])

                    quality = "❌ Generic" if is_generic else "✅ Detailed"

                    print(f"   {Fore.GREEN}✓ {response_time:.2f}s | {quality}")
                    print(f"   {Fore.WHITE}Response: {answer[:100]}...")

                    results.append({
                        'question': question,
                        'response_time': response_time,
                        'success': True,
                        'is_generic': is_generic,
                        'answer_length': len(answer)
                    })
                else:
                    print(f"   {Fore.RED}✗ No answer returned")
                    results.append({
                        'question': question,
                        'response_time': response_time,
                        'success': False,
                        'error': 'No answer'
                    })
            else:
                print(f"   {Fore.RED}✗ HTTP {response.status_code}")
                results.append({
                    'question': question,
                    'response_time': response_time,
                    'success': False,
                    'error': f'HTTP {response.status_code}'
                })

        except Exception as e:
            response_time = time.time() - start_time
            print(f"   {Fore.RED}✗ Error: {str(e)}")
            results.append({
                'question': question,
                'response_time': response_time,
                'success': False,
                'error': str(e)
            })

        print()

    total_time = time.time() - total_start

    # Summary
    print(f"{Fore.CYAN}📊 Quick Benchmark Summary:")
    print("=" * 30)

    successful = [r for r in results if r['success']]
    if successful:
        avg_time = sum(r['response_time'] for r in successful) / len(successful)
        non_generic = [r for r in successful if not r.get('is_generic', True)]

        print(f"✅ Success Rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)")
        print(f"⚡ Average Response Time: {avg_time:.2f}s")
        print(f"🎯 Quality Responses: {len(non_generic)}/{len(successful)} ({len(non_generic)/len(successful)*100:.1f}%)")
        print(f"⏱️  Total Test Time: {total_time:.2f}s")

        # Grade
        if avg_time < 3 and len(non_generic)/len(successful) >= 0.8:
            grade = "🏆 A+"
        elif avg_time < 5 and len(non_generic)/len(successful) >= 0.6:
            grade = "🥇 A"
        elif avg_time < 10 and len(non_generic)/len(successful) >= 0.4:
            grade = "🥈 B"
        else:
            grade = "🥉 C"

        print(f"📈 Overall Grade: {grade}")
    else:
        print(f"{Fore.RED}❌ All tests failed!")

if __name__ == "__main__":
    print(f"{Fore.GREEN}🚀 Starting Quick Benchmark...")

    # Check API
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ API is running")
            quick_benchmark()
        else:
            print(f"{Fore.RED}❌ API not responding")
    except:
        print(f"{Fore.RED}❌ Cannot connect to API - Please start: python api_server.py")
