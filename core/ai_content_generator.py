from models.data_models import LearningStyleProfile, LearningDimension
from typing import Dict, List, Optional
import random


class AIGeneratedContent:
    def __init__(self):
        self.content_cache: Dict[str, str] = {}

    def generate_explanation(
        self,
        topic: str,
        concept: str,
        profile: LearningStyleProfile,
        depth: str = "medium"
    ) -> str:
        if profile.dominant_dimension == LearningDimension.VISUAL:
            return self._generate_visual_explanation(topic, concept, depth)
        elif profile.dominant_dimension == LearningDimension.VERBAL:
            return self._generate_verbal_explanation(topic, concept, depth)
        elif profile.dominant_dimension == LearningDimension.LOGICAL:
            return self._generate_logical_explanation(topic, concept, depth)
        elif profile.dominant_dimension == LearningDimension.PRACTICAL:
            return self._generate_practical_explanation(topic, concept, depth)
        elif profile.dominant_dimension == LearningDimension.SOCIAL:
            return self._generate_social_explanation(topic, concept, depth)
        else:
            return self._generate_mixed_explanation(topic, concept, depth)

    def _generate_visual_explanation(self, topic: str, concept: str, depth: str) -> str:
        return f"""[VISUAL] {topic} - Visual Explanation

[Core Diagram]
[AI generates a diagram showing {concept} relationships]

[Visual Description]
When looking at this diagram, {topic} can be understood as an input-to-output transformation:

+------------+    +----------+    +------------+
|   Input    | -> | {concept[:5]:<8} | -> |   Output   |
+------------+    +----------+    +------------+

[Key Elements]
* Element A (left): Responsible for...
* Element B (center): Core processing...
* Element C (right): Result output...

[Animation Description]
Imagine {topic}'s working process as...
(AI would generate dynamic demonstration here)

[Memory Tip]
Visual mnemonic: "ABC -> 123"
A = Start, B = Process, C = End"""

    def _generate_verbal_explanation(self, topic: str, concept: str, depth: str) -> str:
        detail_prefix = "Detailed" if depth == "high" else ""
        return f"""[VERBAL] {topic} - {detail_prefix} Text Explanation

[Formal Definition]
{topic} refers to...

{concept}, as its core component, has the following characteristics:
1. Characteristic 1: ...
2. Characteristic 2: ...
3. Characteristic 3: ...

[Detailed Explanation]
{detail_prefix} introduction to {topic}'s working principle:

First, we need to understand the essence of {topic}...
Second, in this process, {concept} plays the role of...
Finally, through the synergy of..., ... is achieved

[Terminology]
* {topic} main term: refers to...
* Related term A: defined as...
* Related term B: defined as...

[Knowledge Links]
Related concepts to {topic}:
- Related concept to {concept}: ...
- Extended concept: ...
- Opposite concept: ..."""

    def _generate_logical_explanation(self, topic: str, concept: str, depth: str) -> str:
        return f"""[LOGICAL] {topic} - Logical Derivation

[Mathematical Definition]
Let X be the input set, Y be the output set
Define function f: X -> Y representing the {topic} mapping

[Theorem]
Theorem 1: For any x in X, there exists unique y = f(x) in Y

[Derivation Process]
Proof: Let x1, x2 in X and x1 = x2
 Step 1: By transitive property of equality...
 Step 2: Apply definition of {concept}...
 Step 3: Conclude f(x1) = f(x2) QED

[Logical Structure]
Premise A -> Conclusion B
Premise B + Premise C -> Conclusion D
---------------------------
Therefore: {topic} property holds

[Complexity Analysis]
Time complexity: O(...)
Space complexity: O(...)

[Formal Verification]
For all x in X: P(x) -> Q(x)
Where P(x) denotes..., Q(x) denotes..."""

    def _generate_practical_explanation(self, topic: str, concept: str, depth: str) -> str:
        return f"""[PRACTICAL] {topic} - Practical Application

[Real Scenario]
Imagine you are developing a real project that needs {topic} to solve...

[Code Implementation]
```python
# Python implementation of {topic}
class {concept.title()}Handler:
    def __init__(self):
        self.state = None

    def process(self, input_data):
        # Core processing logic
        result = self._transform(input_data)
        return result

    def _transform(self, data):
        # Data transformation
        return processed_data

# Usage example
handler = {concept.title()}Handler()
output = handler.process(your_input)
```

[Debugging Tips]
When encountering problems:
1. Check if input data format is correct
2. Verify intermediate processing steps
3. Confirm output meets expectations

[Best Practices]
* Error handling: Add exception catching
* Performance: Use caching mechanism
* Code quality: Maintain modular design"""

    def _generate_social_explanation(self, topic: str, concept: str, depth: str) -> str:
        return f"""[SOCIAL] {topic} - Collaborative Learning

[Group Discussion]
Let's understand {topic} in a group format:

**Question 1**: What are the application scenarios of {concept} in real work?

**Viewpoint A**: In project management...
**Viewpoint B**: In technical development...
**Viewpoint C**: In data analysis...

[Diverse Perspectives]
Different angles of understanding:
-> From user perspective: ...
-> From developer perspective: ...
-> From product manager perspective: ...

[Teaching Practice]
Please explain the concept of {topic} to your peers in your own words
(Feynman technique: output drives input)

[Community Resources]
* Recommended reading: Related blog articles
* Discussion topic: Pros and cons of {topic}
* Q&A time: Weekly fixed office hours"""

    def _generate_mixed_explanation(self, topic: str, concept: str, depth: str) -> str:
        return f"""[MIXED] {topic} - Comprehensive Explanation

[Overview]
{topic} is an important concept, and we will learn it from multiple dimensions.

[Theoretical Level]
The basic principle of {concept} is...

[Visualization]
[Comprehensive diagram display]

[Practical Application]
In hands-on practice...

[Reflection Questions]
1. What is the relationship between {topic} and other concepts?
2. How to apply what you learned to real scenarios?

[Extended Learning]
Recommended directions for further exploration: ..."""


class ExerciseGenerator:
    def __init__(self):
        self.exercise_templates: Dict[str, List] = {}

    def generate_practice_exercises(
        self,
        topic: str,
        difficulty: float,
        profile: LearningStyleProfile,
        count: int = 5
    ) -> List[Dict]:
        exercises = []

        if profile.practical_score > 0.6:
            practical = self._generate_practical_exercises(topic, difficulty, count // 2)
            exercises.extend(practical)

        if profile.logical_score > 0.6:
            logical = self._generate_logical_exercises(topic, difficulty, count // 2)
            exercises.extend(logical)

        if profile.visual_score > 0.6:
            visual = self._generate_visual_exercises(topic, difficulty, count // 3)
            exercises.extend(visual)

        remaining = count - len(exercises)
        if remaining > 0:
            conceptual = self._generate_conceptual_exercises(topic, difficulty, remaining)
            exercises.extend(conceptual)

        return exercises[:count]

    def _generate_practical_exercises(self, topic: str, difficulty: float, count: int) -> List[Dict]:
        exercises = []
        templates = [
            {
                "type": "coding",
                "template": "Please implement a {topic} function that calculates...",
                "solution_template": "def {topic_lower}():\\n    pass"
            },
            {
                "type": "application",
                "template": "Given scenario X, apply {topic} to solve the problem...",
                "solution_template": "Step 1: Analyze problem\\nStep 2: Apply {topic}"
            },
            {
                "type": "debug",
                "template": "The following code has errors, please fix...",
                "solution_template": "The error is..."
            }
        ]

        for i in range(count):
            template = templates[i % len(templates)]
            exercises.append({
                "id": f"prac_{topic}_{i}",
                "type": template["type"],
                "question": template["template"].format(topic=topic, topic_lower=topic.lower()),
                "difficulty": difficulty,
                "solution": template["solution_template"].format(topic=topic, topic_lower=topic.lower()),
                "hints": [
                    f"Hint 1: Recall {topic}'s core steps",
                    f"Hint 2: Consider edge cases"
                ]
            })
        return exercises

    def _generate_logical_exercises(self, topic: str, difficulty: float, count: int) -> List[Dict]:
        exercises = []
        templates = [
            {
                "type": "proof",
                "template": "Prove: If premise A holds, then {topic} conclusion B holds",
                "solution_template": "Proof:\\n1. From condition A...\\n2. Apply theorem...\\n3. Draw conclusion"
            },
            {
                "type": "derivation",
                "template": "Derive the mathematical expression for {topic}: Given X=...",
                "solution_template": "From known conditions: X=...\\nSubstitute {topic} definition:...\\nDerivation result:..."
            },
            {
                "type": "analysis",
                "template": "Analyze the time complexity of the {topic} algorithm",
                "solution_template": "Analysis:\\nWorst case: O(n)\\nBest case: O(1)"
            }
        ]

        for i in range(count):
            template = templates[i % len(templates)]
            exercises.append({
                "id": f"logic_{topic}_{i}",
                "type": template["type"],
                "question": template["template"].format(topic=topic),
                "difficulty": difficulty,
                "solution": template["solution_template"].format(topic=topic),
                "hints": [
                    "Hint 1: Recall related theorems",
                    "Hint 2: Consider special cases"
                ]
            })
        return exercises

    def _generate_visual_exercises(self, topic: str, difficulty: float, count: int) -> List[Dict]:
        exercises = []
        templates = [
            {
                "type": "diagram",
                "template": "Please complete the following diagram based on {topic}'s workflow",
                "solution_template": "Complete flowchart:\\n[Diagram]"
            },
            {
                "type": "matching",
                "template": "Connect {topic}'s various elements with their corresponding functions",
                "solution_template": "A->Function 1\\nB->Function 2"
            },
            {
                "type": "identification",
                "template": "Identify key components in the following {topic}-related diagrams",
                "solution_template": "Component 1: Responsible for...\\nComponent 2: Responsible for..."
            }
        ]

        for i in range(count):
            template = templates[i % len(templates)]
            exercises.append({
                "id": f"visual_{topic}_{i}",
                "type": template["type"],
                "question": template["template"].format(topic=topic),
                "difficulty": difficulty,
                "solution": template["solution_template"].format(topic=topic),
                "hints": [
                    "Hint 1: Note the direction of arrows",
                    "Hint 2: Focus on color coding"
                ]
            })
        return exercises

    def _generate_conceptual_exercises(self, topic: str, difficulty: float, count: int) -> List[Dict]:
        exercises = []
        templates = [
            {
                "type": "multiple_choice",
                "template": "Regarding {topic}, which of the following is correct?",
                "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                "correct": 0
            },
            {
                "type": "true_false",
                "template": "True or False: The core principle of {topic} is...",
                "correct": True
            },
            {
                "type": "definition",
                "template": "Please briefly describe the definition of {topic} and its importance",
                "solution_template": "Definition:...\\nImportance:..."
            }
        ]

        for i in range(count):
            template = templates[i % len(templates)]
            exercise = {
                "id": f"conc_{topic}_{i}",
                "type": template["type"],
                "question": template["template"].format(topic=topic),
                "difficulty": difficulty
            }
            if "options" in template:
                exercise["options"] = template["options"]
                exercise["correct"] = template["correct"]
            if "solution_template" in template:
                exercise["solution"] = template["solution_template"].format(topic=topic)
            exercises.append(exercise)
        return exercises

    def generate_quiz(
        self,
        topics: List[str],
        profile: LearningStyleProfile,
        question_count: int = 10
    ) -> Dict:
        all_exercises = []
        per_topic = max(1, question_count // len(topics))

        for topic in topics:
            exercises = self.generate_practice_exercises(
                topic,
                difficulty=0.5,
                profile=profile,
                count=per_topic
            )
            all_exercises.extend(exercises)

        random.shuffle(all_exercises)

        return {
            "quiz_id": f"quiz_{'_'.join(topics)}",
            "topics": topics,
            "questions": all_exercises[:question_count],
            "time_limit": len(all_exercises) * 2,
            "passing_score": 0.7
        }

    def evaluate_answer(
        self,
        exercise: Dict,
        user_answer: any
    ) -> Dict:
        result = {
            "correct": False,
            "score": 0.0,
            "feedback": "",
            "explanation": ""
        }

        exercise_type = exercise.get("type")

        if exercise_type in ["multiple_choice", "true_false"]:
            correct = exercise.get("correct")
            if exercise_type == "multiple_choice":
                result["correct"] = user_answer == correct
            else:
                result["correct"] = user_answer == correct
            result["score"] = 1.0 if result["correct"] else 0.0

        elif exercise_type == "coding":
            result["score"] = self._evaluate_code(exercise, user_answer)
            result["correct"] = result["score"] >= 0.7
            result["explanation"] = exercise.get("solution", "")

        else:
            result["feedback"] = "Please analyze using the solution below"

        if not result["correct"]:
            result["feedback"] = self._generate_incorrect_feedback(exercise)
        else:
            result["feedback"] = "Correct!"

        return result

    def _evaluate_code(self, exercise: Dict, user_code: str) -> float:
        basic_score = 0.3
        return basic_score + 0.4

    def _generate_incorrect_feedback(self, exercise: Dict) -> str:
        feedbacks = [
            "This answer is not quite right, let's think again...",
            "Need more thinking, try analyzing from another angle",
            "Recommend reviewing related knowledge before trying again",
            "The solution's approach may help you"
        ]
        return random.choice(feedbacks)
