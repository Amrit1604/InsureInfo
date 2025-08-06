"""
🧪 ACCURACY AND SPEED TEST SUITE
================================
Comprehensive testing for the LLM Claims Processing API
Tests response accuracy, speed, and quality metrics

Usage:
    python accuracy_speed_test.py
"""

import requests
import json
import time
import statistics
from datetime import datetime
from typing import List, Dict, Any
import os
from colorama import init, Fore, Back, Style

# Initialize colorama for colored output
init(autoreset=True)

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []

    def run_comprehensive_test(self):
        """Run all test categories"""
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}")
        print("🧪 LLM CLAIMS PROCESSING - ACCURACY & SPEED TEST")
        print("=" * 50)
        print(f"{Style.RESET_ALL}")

        # Test categories
        test_categories = [
            ("Simple Questions", self.get_simple_test_questions()),
            ("Complex Scenarios", self.get_complex_test_questions()),
            ("Emergency Cases", self.get_emergency_test_questions()),
            ("Edge Cases", self.get_edge_case_questions()),
            ("Real World Cases", self.get_real_world_questions())
        ]

        all_results = {}

        for category_name, questions in test_categories:
            print(f"\n{Fore.CYAN}🔍 Testing Category: {Style.BRIGHT}{category_name}")
            print(f"{Fore.CYAN}{'─' * 40}")

            results = self.test_question_set(questions, category_name)
            all_results[category_name] = results

            # Display category summary
            self.display_category_summary(category_name, results)

        # Overall summary
        self.display_overall_summary(all_results)

        # Save detailed results
        self.save_results_to_file(all_results)

        return all_results

    def test_question_set(self, questions: List[Dict], category: str) -> Dict:
        """Test a set of questions and return metrics"""
        results = {
            'questions_tested': len(questions),
            'response_times': [],
            'accuracy_scores': [],
            'quality_scores': [],
            'detailed_results': []
        }

        for i, test_case in enumerate(questions, 1):
            print(f"{Fore.YELLOW}  {i}. Testing: {test_case['question'][:60]}...")

            # Measure response time and get result
            start_time = time.time()
            response = self.call_api(test_case['question'])
            response_time = time.time() - start_time

            if response:
                # Evaluate response quality
                accuracy_score = self.evaluate_accuracy(test_case, response)
                quality_score = self.evaluate_quality(response)

                results['response_times'].append(response_time)
                results['accuracy_scores'].append(accuracy_score)
                results['quality_scores'].append(quality_score)

                # Store detailed result
                detailed_result = {
                    'question': test_case['question'],
                    'expected_decision': test_case.get('expected_decision', 'unknown'),
                    'expected_keywords': test_case.get('expected_keywords', []),
                    'actual_response': response,
                    'response_time': response_time,
                    'accuracy_score': accuracy_score,
                    'quality_score': quality_score
                }
                results['detailed_results'].append(detailed_result)

                # Display result
                status_color = Fore.GREEN if accuracy_score >= 7 else Fore.YELLOW if accuracy_score >= 5 else Fore.RED
                print(f"     {status_color}✓ Response: {response_time:.2f}s | Accuracy: {accuracy_score}/10 | Quality: {quality_score}/10")

            else:
                print(f"     {Fore.RED}✗ API call failed")
                results['detailed_results'].append({
                    'question': test_case['question'],
                    'error': 'API call failed',
                    'response_time': response_time,
                    'accuracy_score': 0,
                    'quality_score': 0
                })

        return results

    def call_api(self, question: str) -> str:
        """Call the API with a single question"""
        try:
            payload = {
                "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
                "questions": [question]
            }

            response = requests.post(
                f"{self.base_url}/hackrx/run",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120  # 2 minute timeout for complex questions
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('answers') and len(data['answers']) > 0:
                    return data['answers'][0]['answer']

            return None

        except Exception as e:
            print(f"     {Fore.RED}API Error: {str(e)}")
            return None

    def evaluate_accuracy(self, test_case: Dict, response: str) -> int:
        """Evaluate response accuracy (1-10 scale)"""
        score = 5  # Base score

        # Check for expected keywords
        expected_keywords = test_case.get('expected_keywords', [])
        for keyword in expected_keywords:
            if keyword.lower() in response.lower():
                score += 1

        # Check for generic/error responses (negative points)
        generic_phrases = [
            "sorry, there was an error",
            "contact customer service",
            "unable to process",
            "no explanation available"
        ]

        for phrase in generic_phrases:
            if phrase.lower() in response.lower():
                score -= 2

        # Check for detailed analysis (positive points)
        detail_indicators = [
            "based on policy",
            "clause",
            "coverage",
            "₹",  # Currency symbol
            "percentage",
            "emergency",
            "medical necessity"
        ]

        detail_count = sum(1 for indicator in detail_indicators if indicator.lower() in response.lower())
        score += min(detail_count, 3)  # Max 3 bonus points

        return max(1, min(10, score))  # Clamp between 1-10

    def evaluate_quality(self, response: str) -> int:
        """Evaluate response quality (1-10 scale)"""
        score = 5  # Base score

        # Length check (not too short, not too long)
        if 100 <= len(response) <= 1000:
            score += 1
        elif len(response) < 50:
            score -= 2

        # Structure and helpfulness
        if any(phrase in response.lower() for phrase in ["next steps", "recommendation", "contact"]):
            score += 1

        # Medical/insurance terminology
        medical_terms = ["medical", "treatment", "policy", "coverage", "claim", "diagnosis"]
        term_count = sum(1 for term in medical_terms if term.lower() in response.lower())
        score += min(term_count, 2)

        # Coherence check (no obvious errors)
        if "error" not in response.lower() or "based on policy documents" in response.lower():
            score += 1

        return max(1, min(10, score))

    def display_category_summary(self, category: str, results: Dict):
        """Display summary for a test category"""
        if not results['response_times']:
            print(f"     {Fore.RED}No successful tests in this category")
            return

        avg_time = statistics.mean(results['response_times'])
        avg_accuracy = statistics.mean(results['accuracy_scores'])
        avg_quality = statistics.mean(results['quality_scores'])

        print(f"\n     {Fore.CYAN}📊 {category} Summary:")
        print(f"     Average Response Time: {Fore.YELLOW}{avg_time:.2f}s")
        print(f"     Average Accuracy: {Fore.YELLOW}{avg_accuracy:.1f}/10")
        print(f"     Average Quality: {Fore.YELLOW}{avg_quality:.1f}/10")
        print(f"     Success Rate: {Fore.YELLOW}{len(results['response_times'])}/{results['questions_tested']} ({len(results['response_times'])/results['questions_tested']*100:.1f}%)")

    def display_overall_summary(self, all_results: Dict):
        """Display comprehensive test summary"""
        print(f"\n{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}")
        print("📈 OVERALL TEST SUMMARY")
        print("=" * 30)
        print(f"{Style.RESET_ALL}")

        total_tests = sum(r['questions_tested'] for r in all_results.values())
        total_successful = sum(len(r['response_times']) for r in all_results.values())

        all_times = []
        all_accuracy = []
        all_quality = []

        for results in all_results.values():
            all_times.extend(results['response_times'])
            all_accuracy.extend(results['accuracy_scores'])
            all_quality.extend(results['quality_scores'])

        if all_times:
            print(f"{Fore.CYAN}🎯 Performance Metrics:")
            print(f"   Total Tests: {Fore.YELLOW}{total_tests}")
            print(f"   Successful Tests: {Fore.YELLOW}{total_successful} ({total_successful/total_tests*100:.1f}%)")
            print(f"   Average Response Time: {Fore.YELLOW}{statistics.mean(all_times):.2f}s")
            print(f"   Fastest Response: {Fore.GREEN}{min(all_times):.2f}s")
            print(f"   Slowest Response: {Fore.RED}{max(all_times):.2f}s")

            print(f"\n{Fore.CYAN}🎯 Quality Metrics:")
            print(f"   Average Accuracy Score: {Fore.YELLOW}{statistics.mean(all_accuracy):.1f}/10")
            print(f"   Average Quality Score: {Fore.YELLOW}{statistics.mean(all_quality):.1f}/10")

            # Performance grades
            avg_time = statistics.mean(all_times)
            avg_accuracy = statistics.mean(all_accuracy)

            speed_grade = "A+" if avg_time < 3 else "A" if avg_time < 5 else "B" if avg_time < 10 else "C"
            accuracy_grade = "A+" if avg_accuracy >= 8 else "A" if avg_accuracy >= 7 else "B" if avg_accuracy >= 6 else "C"

            print(f"\n{Fore.CYAN}🏆 Performance Grades:")
            print(f"   Speed Grade: {Fore.YELLOW}{speed_grade}")
            print(f"   Accuracy Grade: {Fore.YELLOW}{accuracy_grade}")

    def save_results_to_file(self, all_results: Dict):
        """Save detailed results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"

        # Prepare data for JSON serialization
        serializable_results = {}
        for category, results in all_results.items():
            serializable_results[category] = {
                'questions_tested': results['questions_tested'],
                'avg_response_time': statistics.mean(results['response_times']) if results['response_times'] else 0,
                'avg_accuracy_score': statistics.mean(results['accuracy_scores']) if results['accuracy_scores'] else 0,
                'avg_quality_score': statistics.mean(results['quality_scores']) if results['quality_scores'] else 0,
                'success_rate': len(results['response_times']) / results['questions_tested'] * 100 if results['questions_tested'] > 0 else 0,
                'detailed_results': results['detailed_results']
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)

        print(f"\n{Fore.GREEN}💾 Detailed results saved to: {filename}")

    def get_simple_test_questions(self) -> List[Dict]:
        """Simple, straightforward questions"""
        return [
            {
                "question": "What is the grace period for premium payment?",
                "expected_keywords": ["grace period", "premium", "days"],
                "expected_decision": "informational"
            },
            {
                "question": "Does this policy cover dental treatment?",
                "expected_keywords": ["dental", "coverage", "treatment"],
                "expected_decision": "informational"
            },
            {
                "question": "What is the waiting period for pre-existing diseases?",
                "expected_keywords": ["waiting period", "pre-existing", "diseases"],
                "expected_decision": "informational"
            },
            {
                "question": "I broke my arm, am I covered?",
                "expected_keywords": ["injury", "coverage", "approved"],
                "expected_decision": "approved"
            },
            {
                "question": "What is the maximum coverage amount?",
                "expected_keywords": ["maximum", "coverage", "amount", "₹"],
                "expected_decision": "informational"
            }
        ]

    def get_complex_test_questions(self) -> List[Dict]:
        """Complex scenarios requiring detailed analysis"""
        return [
            {
                "question": "I am a 45-year-old diabetic patient who suffered a heart attack while traveling. My policy is 2 years old. Will my ₹5,00,000 treatment be covered considering my pre-existing diabetes?",
                "expected_keywords": ["diabetes", "heart attack", "pre-existing", "coverage", "emergency"],
                "expected_decision": "approved"
            },
            {
                "question": "My wife needs emergency C-section delivery at 7 months pregnancy. We have maternity coverage for 18 months. What percentage will be covered for NICU care?",
                "expected_keywords": ["maternity", "emergency", "C-section", "NICU", "coverage", "percentage"],
                "expected_decision": "approved"
            },
            {
                "question": "I need experimental cancer treatment costing ₹15,00,000. My policy has ₹10,00,000 coverage with cancer rider. What are my options?",
                "expected_keywords": ["cancer", "experimental", "rider", "coverage", "options", "₹"],
                "expected_decision": "requires_review"
            }
        ]

    def get_emergency_test_questions(self) -> List[Dict]:
        """Emergency scenarios requiring immediate response"""
        return [
            {
                "question": "URGENT: Heart attack patient needs immediate surgery. Policy holder for 6 months. Please approve emergency treatment.",
                "expected_keywords": ["emergency", "heart attack", "surgery", "immediate", "approved"],
                "expected_decision": "approved"
            },
            {
                "question": "Emergency stroke case - patient unconscious, need ICU admission immediately. 3-year policy holder.",
                "expected_keywords": ["emergency", "stroke", "ICU", "immediate", "approved"],
                "expected_decision": "approved"
            },
            {
                "question": "Critical accident case - multiple injuries, emergency surgery required. Please fast-track approval.",
                "expected_keywords": ["emergency", "accident", "critical", "surgery", "fast-track"],
                "expected_decision": "approved"
            }
        ]

    def get_edge_case_questions(self) -> List[Dict]:
        """Edge cases and unusual scenarios"""
        return [
            {
                "question": "What about treatment in Antarctica for emergency appendicitis?",
                "expected_keywords": ["emergency", "treatment", "location", "coverage"],
                "expected_decision": "requires_review"
            },
            {
                "question": "Policy purchased yesterday, heart attack today. Pre-existing or emergency?",
                "expected_keywords": ["pre-existing", "emergency", "waiting period", "new policy"],
                "expected_decision": "requires_review"
            },
            {
                "question": "Treatment cost is ₹50,00,000 but my coverage is only ₹5,00,000. What happens?",
                "expected_keywords": ["coverage limit", "excess", "₹", "options"],
                "expected_decision": "partial"
            }
        ]

    def get_real_world_questions(self) -> List[Dict]:
        """Real-world complex scenarios from the test file"""
        return [
            {
                "question": "I am a 45-year-old diabetic patient who has been managing my condition with insulin for 8 years. Last month, while traveling for business in a different state, I suffered a severe hypoglycemic episode that led to unconsciousness and required emergency hospitalization for 3 days including ICU admission. The hospital performed comprehensive tests including cardiac monitoring, neurological assessments, and endocrine consultations. My policy has been active for 18 months. The total bill is ₹2,50,000 including room charges, specialist consultations, diagnostic tests, and medications. The treating physician has recommended follow-up with an endocrinologist and cardiologist due to complications. Will this claim be covered considering my pre-existing diabetes, the out-of-state treatment, the emergency nature, and the comprehensive care required? What percentage of the bill will be covered and are there any specific exclusions I should be aware of?",
                "expected_keywords": ["diabetes", "emergency", "ICU", "coverage", "percentage", "exclusions"],
                "expected_decision": "approved"
            },
            {
                "question": "I am a 52-year-old construction worker who was recently diagnosed with mesothelioma, a rare cancer caused by asbestos exposure from my work over the past 25 years. My oncologist has recommended a comprehensive treatment plan including surgical resection, chemotherapy, and radiation therapy, with estimated costs exceeding ₹25,00,000 over the next 18 months. The treatment requires specialized care at a cancer center, including experimental immunotherapy protocols that may not be covered under standard policies. Additionally, I need to travel 800 kilometers to reach the nearest specialized mesothelioma treatment center, requiring temporary relocation for my family. My current health insurance policy has a sum insured of ₹10,00,000 with cancer coverage as a rider. The insurance company is questioning whether this is a pre-existing condition since mesothelioma has a long latency period and symptoms may have been present before policy inception, though undiagnosed. They are also questioning coverage for experimental treatments and travel/accommodation expenses. Given the occupational nature of this disease, the specialized treatment requirements, the inadequate sum insured amount, and the dispute over pre-existing conditions, what are my legal rights? Can I claim compensation from my employer's liability insurance? What specific steps should I take to ensure maximum coverage from my health insurance, and are there government schemes or cancer foundations that can supplement the treatment costs?",
                "expected_keywords": ["mesothelioma", "cancer", "occupational", "experimental", "legal rights", "compensation"],
                "expected_decision": "requires_review"
            }
        ]

def main():
    """Main function to run the test suite"""
    print(f"{Fore.GREEN}🚀 Starting API Accuracy & Speed Test Suite...")

    # Check if API is running
    tester = APITester()
    try:
        response = requests.get(f"{tester.base_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"{Fore.RED}❌ API not responding at {tester.base_url}")
            print(f"{Fore.YELLOW}💡 Please start the API server first: python api_server.py")
            return
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}❌ Cannot connect to API at {tester.base_url}")
        print(f"{Fore.YELLOW}💡 Please start the API server first: python api_server.py")
        return

    print(f"{Fore.GREEN}✅ API is running, starting tests...")

    # Run comprehensive test suite
    results = tester.run_comprehensive_test()

    print(f"\n{Fore.GREEN}🎉 Test suite completed!")
    print(f"{Fore.CYAN}📁 Check the generated test_results_*.json file for detailed analysis")

if __name__ == "__main__":
    main()
