"""
🏥 INTELLIGENT CLAIMS PROCESSOR - COMPREHENSIVE DEMO
===================================================
This demo showcases the full capabilities of our LLM-powered
insurance claims processing system.
"""

from main import IntelligentClaimsProcessor
from colorama import init, Fore, Back, Style
import time

# Initialize colorama
init(autoreset=True)

def run_comprehensive_demo():
    """Run a comprehensive demonstration of the system"""

    print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}")
    print("🏥 INTELLIGENT INSURANCE CLAIMS PROCESSING SYSTEM")
    print("=================================================")
    print("Comprehensive Demo - Natural Language to Claims Decisions")
    print(f"{Style.RESET_ALL}")

    # Initialize the processor
    print(f"\n{Fore.YELLOW}🚀 Initializing the AI Claims Processor...")
    processor = IntelligentClaimsProcessor()

    # Load documents
    print(f"\n{Fore.CYAN}📚 Loading policy documents...")
    if not processor.load_documents("docs"):
        print(f"{Fore.RED}❌ Failed to load documents. Please ensure sample_policy_merged.pdf is in the docs folder.")
        return

    print(f"\n{Fore.GREEN}✅ System ready! Now demonstrating various claim scenarios...")

    # Test cases covering different scenarios
    test_cases = [
        {
            "title": "Middle-aged Male Knee Surgery",
            "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
            "description": "Standard orthopedic procedure for middle-aged patient"
        },
        {
            "title": "Child Sports Injury",
            "query": "my kid broke his arm playing soccer we have insurance for 2 years",
            "description": "Casual language for pediatric fracture with established policy"
        },
        {
            "title": "Young Adult Emergency Surgery",
            "query": "25F, appendix surgery, Mumbai, 1 year policy",
            "description": "Emergency appendectomy for young female"
        },
        {
            "title": "Senior Emergency Heart Attack",
            "query": "emergency heart attack, 55 year old man, 6 month policy",
            "description": "Critical cardiac emergency for senior citizen"
        },
        {
            "title": "Routine Dental Care",
            "query": "dental cleaning, 30 years old, 2 year policy",
            "description": "Preventive dental care with mature policy"
        },
        {
            "title": "Vague Injury Description",
            "query": "I hurt my back lifting something heavy, been insured for 8 months",
            "description": "Ambiguous injury description requiring AI interpretation"
        },
        {
            "title": "Pre-existing Condition Check",
            "query": "diabetes treatment, 45 year old, just got insurance last month",
            "description": "Testing pre-existing condition detection"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{Back.MAGENTA}{Fore.WHITE}")
        print(f"📋 TEST CASE {i}/{len(test_cases)}: {test_case['title']}")
        print(f"Description: {test_case['description']}")
        print(f"Query: '{test_case['query']}'")
        print(f"{Style.RESET_ALL}")

        # Process the claim
        start_time = time.time()
        decision = processor.process_claim_query(test_case['query'])
        processing_time = time.time() - start_time

        # Display results
        processor.display_decision(decision)

        print(f"{Fore.MAGENTA}⏱️  Processing Time: {processing_time:.2f} seconds")

        # Store results for summary
        results.append({
            'case': test_case['title'],
            'query': test_case['query'],
            'decision': decision['decision'],
            'amount': decision.get('amount'),
            'time': processing_time
        })

        # Wait before next test
        if i < len(test_cases):
            print(f"\n{Fore.YELLOW}⏳ Preparing next test case...")
            time.sleep(2)

    # Summary report
    print_summary_report(results)

def print_summary_report(results):
    """Print a comprehensive summary of all test results"""

    print(f"\n{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}")
    print("📊 COMPREHENSIVE DEMO SUMMARY REPORT")
    print("=====================================")
    print(f"{Style.RESET_ALL}")

    # Statistics
    total_cases = len(results)
    approved_cases = sum(1 for r in results if r['decision'] == 'approved')
    rejected_cases = sum(1 for r in results if r['decision'] == 'rejected')
    error_cases = sum(1 for r in results if r['decision'] == 'error')
    avg_time = sum(r['time'] for r in results) / total_cases

    print(f"{Fore.CYAN}📈 STATISTICS:")
    print(f"   • Total test cases: {total_cases}")
    print(f"   • {Fore.GREEN}Approved: {approved_cases} ({approved_cases/total_cases*100:.1f}%)")
    print(f"   • {Fore.RED}Rejected: {rejected_cases} ({rejected_cases/total_cases*100:.1f}%)")
    print(f"   • {Fore.YELLOW}Errors: {error_cases} ({error_cases/total_cases*100:.1f}%)")
    print(f"   • Average processing time: {avg_time:.2f} seconds")

    print(f"\n{Fore.BLUE}📋 DETAILED RESULTS:")
    for i, result in enumerate(results, 1):
        status_color = Fore.GREEN if result['decision'] == 'approved' else Fore.RED if result['decision'] == 'rejected' else Fore.YELLOW
        status_icon = "✅" if result['decision'] == 'approved' else "❌" if result['decision'] == 'rejected' else "⚠️"

        print(f"   {i}. {result['case']}")
        print(f"      Query: \"{result['query'][:50]}{'...' if len(result['query']) > 50 else ''}\"")
        print(f"      Result: {status_color}{status_icon} {result['decision'].upper()}{Style.RESET_ALL}")
        if result['amount']:
            print(f"      Amount: ₹{result['amount']:,}")
        print(f"      Time: {result['time']:.2f}s")
        print()

    # System capabilities demonstrated
    print(f"{Fore.MAGENTA}🎯 CAPABILITIES DEMONSTRATED:")
    capabilities = [
        "✅ Natural language understanding (casual to formal medical terms)",
        "✅ Age and policy duration analysis",
        "✅ Emergency detection and fast-track processing",
        "✅ Semantic search through policy documents",
        "✅ AI-powered decision making with justifications",
        "✅ Coverage vs procedural requirement distinction",
        "✅ Pre-existing condition detection",
        "✅ Structured JSON output for downstream systems"
    ]

    for capability in capabilities:
        print(f"   {capability}")

    print(f"\n{Fore.GREEN}🎉 Demo completed successfully!")
    print(f"The system demonstrates robust natural language processing")
    print(f"and intelligent decision-making for insurance claims.")

def interactive_mode():
    """Run interactive mode for custom queries"""

    print(f"\n{Back.CYAN}{Fore.WHITE}")
    print("💬 INTERACTIVE MODE")
    print("===================")
    print("Enter your own claim queries to test the system")
    print(f"{Style.RESET_ALL}")

    processor = IntelligentClaimsProcessor()
    if not processor.load_documents("docs"):
        print(f"{Fore.RED}❌ Failed to load documents.")
        return

    print(f"\n{Fore.GREEN}🚀 Interactive system ready!")
    print(f"{Fore.WHITE}Enter 'demo' to run the comprehensive demo again")
    print(f"Enter 'quit' to exit")

    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}Enter your claim query: {Fore.WHITE}")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.GREEN}👋 Thank you for using the Intelligent Claims Processor!")
                break
            elif user_input.lower() == 'demo':
                run_comprehensive_demo()
                continue

            if user_input.strip():
                print(f"\n{Fore.YELLOW}🔄 Processing your query...")
                decision = processor.process_claim_query(user_input)
                processor.display_decision(decision)
            else:
                print(f"{Fore.YELLOW}Please enter a valid claim query.")

        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")

if __name__ == "__main__":
    print(f"{Fore.YELLOW}Choose demo mode:")
    print(f"1. Comprehensive Demo (automated test cases)")
    print(f"2. Interactive Mode (enter your own queries)")
    print(f"3. Both (demo first, then interactive)")

    choice = input(f"\n{Fore.CYAN}Enter your choice (1/2/3): {Fore.WHITE}")

    if choice == "1":
        run_comprehensive_demo()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        run_comprehensive_demo()
        interactive_mode()
    else:
        print(f"{Fore.GREEN}Running comprehensive demo by default...")
        run_comprehensive_demo()
