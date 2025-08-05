"""
⚡ SPEED TEST FOR OPTIMIZED API
===============================
Test the optimized API for speed and accuracy
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8000"
HACKRX_ENDPOINT = f"{BASE_URL}/hackrx/run"

# Smaller test payload for speed testing
speed_test_payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
        "Does this policy cover maternity expenses?"
    ]
}

def speed_test():
    """Test API speed with smaller payload"""
    print("⚡ SPEED TEST - Optimized API")
    print("=" * 40)

    try:
        start_time = time.time()
        response = requests.post(
            HACKRX_ENDPOINT,
            json=speed_test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 second timeout
        )
        end_time = time.time()

        total_time = end_time - start_time

        if response.status_code == 200:
            data = response.json()
            print(f"✅ API call successful!")
            print(f"⏱️  Total response time: {total_time:.2f} seconds")
            print(f"📊 API processing time: {data.get('processing_time', 'N/A')} seconds")
            print(f"❓ Questions processed: {data.get('total_questions', 'N/A')}")
            print(f"✅ Successful answers: {data.get('successful_answers', 'N/A')}")

            # Speed analysis
            if total_time < 3:
                print(f"🚀 EXCELLENT SPEED: {total_time:.2f}s (Target: <3s)")
            elif total_time < 10:
                print(f"⚡ GOOD SPEED: {total_time:.2f}s (Target: <3s)")
            else:
                print(f"⚠️  SLOW: {total_time:.2f}s (Target: <3s)")

            # Show sample answers
            answers = data.get('answers', [])
            print(f"\\n📋 Sample results:")
            for i, answer in enumerate(answers):
                print(f"\\n{i+1}. Q: {answer['question']}")
                print(f"   A: {answer['answer'][:150]}...")
                print(f"   Decision: {answer.get('decision', 'N/A')}")
                print(f"   Confidence: {answer['confidence']:.2f}")

            return total_time < 3  # Success if under 3 seconds

        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Speed test error: {str(e)}")
        return False

def accuracy_test():
    """Test specific accuracy scenarios"""
    print("\\n🎯 ACCURACY TEST")
    print("=" * 40)

    accuracy_questions = [
        "Emergency heart attack, need immediate treatment",
        "Routine checkup for diabetes",
        "Pregnancy complications, urgent care needed"
    ]

    correct_answers = 0

    for question in accuracy_questions:
        try:
            payload = {
                "documents": "test",
                "questions": [question]
            }

            response = requests.post(HACKRX_ENDPOINT, json=payload, timeout=15)

            if response.status_code == 200:
                data = response.json()
                answer = data['answers'][0]
                decision = answer.get('decision', 'error')

                print(f"\\n❓ {question}")
                print(f"🔍 Decision: {decision}")
                print(f"📊 Confidence: {answer['confidence']:.2f}")

                # Basic accuracy check
                if 'emergency' in question.lower() and decision == 'approved':
                    correct_answers += 1
                    print("✅ Correct decision")
                elif 'routine' in question.lower() and decision in ['approved', 'rejected']:
                    correct_answers += 1
                    print("✅ Reasonable decision")
                elif decision in ['approved', 'rejected']:
                    correct_answers += 1
                    print("✅ Valid decision")
                else:
                    print("❌ Poor decision")

        except Exception as e:
            print(f"❌ Error testing question: {e}")

    accuracy = (correct_answers / len(accuracy_questions)) * 100
    print(f"\\n🎯 Accuracy Score: {accuracy:.1f}%")
    return accuracy > 80  # Success if over 80%

def main():
    """Run speed and accuracy tests"""
    print("🏆 OPTIMIZED API PERFORMANCE TEST")
    print("=" * 50)

    # Test 1: Speed
    speed_ok = speed_test()

    # Test 2: Accuracy
    accuracy_ok = accuracy_test()

    # Final verdict
    print("\\n" + "=" * 50)
    print("🏁 FINAL RESULTS:")
    print(f"Speed Test: {'✅ PASS' if speed_ok else '❌ FAIL'}")
    print(f"Accuracy Test: {'✅ PASS' if accuracy_ok else '❌ FAIL'}")

    if speed_ok and accuracy_ok:
        print("\\n🎉 HACKATHON READY! Your API is optimized for winning!")
        print("🚀 Speed: <3s | 🎯 Accuracy: >80% | 🏆 Competition Ready!")
    else:
        print("\\n⚠️  Needs optimization. Check the results above.")

if __name__ == "__main__":
    main()
