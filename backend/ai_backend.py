from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import sqlite3
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

print("🚀 Starting AI-Powered Smart Task Planner...")

class AITaskPlanner:
    def __init__(self):
        # Initialize OpenAI client with error handling
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=api_key)
        
        # Test the connection
        try:
            # Simple test to verify API key works
            self.client.models.list()
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
            raise

    def generate_ai_plan(self, goal, start_date, end_date):
        """Generate intelligent plan using AI"""
        try:
            total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
            
            # AI prompt for intelligent planning
            prompt = f"""
            Create a detailed, actionable task breakdown for the following goal:
            
            GOAL: {goal}
            TIMELINE: {total_days} days (from {start_date} to {end_date})
            
            Please provide:
            1. A domain/category for this goal
            2. 6-8 specific, actionable tasks with:
               - Clear descriptions
               - Realistic durations in days
               - Priority levels (high/medium/low)
               - Logical dependencies
               - Relevant categories
            
            Format as JSON:
            {{
                "domain": "domain_name",
                "tasks": [
                    {{
                        "id": 1,
                        "description": "specific task description",
                        "category": "task category",
                        "priority": "high/medium/low", 
                        "duration_days": number,
                        "dependencies": []
                    }}
                ]
            }}
            
            Make tasks realistic for {total_days} days total.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert project planner and productivity coach. Create realistic, actionable task plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            ai_response = response.choices[0].message.content
            print("🤖 AI Response:", ai_response)
            
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                plan_data = json.loads(json_match.group())
                return self._schedule_tasks_with_dates(plan_data['tasks'], goal, start_date, end_date, plan_data.get('domain', 'AI Generated'))
            else:
                raise Exception("AI response format error")
                
        except Exception as e:
            print(f"❌ AI Planning failed: {e}")
            # Fallback to rule-based planning
            return self._create_fallback_plan(goal, start_date, end_date, total_days)

    def _create_fallback_plan(self, goal, start_date, end_date, total_days):
        """Fallback rule-based planning if AI fails"""
        tasks = [
            self._create_task(1, "Research and information gathering", "Research", "high", max(2, total_days // 6), []),
            self._create_task(2, "Define clear objectives and milestones", "Planning", "high", max(1, total_days // 8), [1]),
            self._create_task(3, "Gather necessary resources", "Preparation", "medium", max(1, total_days // 10), [2]),
            self._create_task(4, "Execute main implementation phase", "Execution", "high", max(4, total_days // 3), [3]),
            self._create_task(5, "Review progress and make adjustments", "Review", "medium", max(2, total_days // 6), [4]),
            self._create_task(6, "Finalize and complete project", "Completion", "high", max(1, total_days // 8), [5])
        ]
        
        return self._schedule_tasks_with_dates(tasks, goal, start_date, end_date, "General Project")

    def _create_task(self, task_id, description, category, priority, duration_days, dependencies):
        """Create a standardized task object"""
        return {
            'id': task_id,
            'description': description,
            'category': category,
            'priority': priority,
            'duration_days': max(1, duration_days),
            'dependencies': dependencies,
            'completed': False
        }

    def _schedule_tasks_with_dates(self, tasks, goal, start_date, end_date, domain):
        """Schedule tasks with actual dates considering dependencies"""
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        total_days = (end_dt - start_dt).days
        
        # Create task dictionary for easy access
        task_dict = {task['id']: task for task in tasks}
        
        # Calculate earliest start dates considering dependencies
        for task in tasks:
            if task['dependencies']:
                dep_end_dates = []
                for dep_id in task['dependencies']:
                    if dep_id in task_dict and 'end_date' in task_dict[dep_id]:
                        dep_end_dates.append(datetime.strptime(task_dict[dep_id]['end_date'], '%Y-%m-%d'))
                
                if dep_end_dates:
                    earliest_start = max(dep_end_dates)
                    task['start_date'] = earliest_start.strftime('%Y-%m-%d')
                else:
                    task['start_date'] = start_date
            else:
                task['start_date'] = start_date
        
        # Schedule tasks
        scheduled_tasks = []
        processed_tasks = set()
        
        while len(processed_tasks) < len(tasks):
            for task in tasks:
                if task['id'] in processed_tasks:
                    continue
                    
                dependencies_met = all(dep_id in processed_tasks for dep_id in task['dependencies'])
                if dependencies_met or not task['dependencies']:
                    start_dt = datetime.strptime(task['start_date'], '%Y-%m-%d')
                    
                    if task['dependencies']:
                        dep_end_dates = []
                        for dep_id in task['dependencies']:
                            dep_task = next((t for t in scheduled_tasks if t['id'] == dep_id), None)
                            if dep_task:
                                dep_end_dates.append(datetime.strptime(dep_task['end_date'], '%Y-%m-%d'))
                        
                        if dep_end_dates:
                            latest_dep_end = max(dep_end_dates)
                            if latest_dep_end > start_dt:
                                start_dt = latest_dep_end
                    
                    end_dt = start_dt + timedelta(days=task['duration_days'])
                    
                    if end_dt > datetime.strptime(end_date, '%Y-%m-%d'):
                        available_days = (datetime.strptime(end_date, '%Y-%m-%d') - start_dt).days
                        task['duration_days'] = max(1, available_days)
                        end_dt = start_dt + timedelta(days=task['duration_days'])
                    
                    task['start_date'] = start_dt.strftime('%Y-%m-%d')
                    task['end_date'] = end_dt.strftime('%Y-%m-%d')
                    task['deadline'] = end_dt.strftime('%Y-%m-%d')
                    
                    scheduled_tasks.append(task)
                    processed_tasks.add(task['id'])
        
        return {
            "goal": goal,
            "domain": domain,
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "tasks": scheduled_tasks,
            "total_tasks": len(scheduled_tasks),
            "ai_generated": True,
            "generated_at": datetime.now().isoformat()
        }

    def regenerate_with_ai(self, original_plan, completed_tasks, feedback=""):
        """Regenerate plan using AI with progress context"""
        try:
            completed_descriptions = [f"Completed: {task['description']}" for task in completed_tasks]
            remaining_goal = original_plan['goal']
            
            prompt = f"""
            Original goal: {remaining_goal}
            Timeline: {original_plan['total_days']} days total
            Current date: {datetime.now().strftime('%Y-%m-%d')}
            
            Already completed:
            {chr(10).join(completed_descriptions)}
            
            User feedback: {feedback if feedback else 'No specific feedback'}
            
            Please create an updated plan for the REMAINING work, considering:
            - What's already been accomplished
            - Remaining timeline
            - Any user feedback
            
            Provide 4-6 remaining tasks in JSON format.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an adaptive project planner. Update plans based on progress and feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            
            if json_match:
                new_plan_data = json.loads(json_match.group())
                # Merge with completed tasks
                all_tasks = completed_tasks + new_plan_data['tasks']
                # Re-number tasks
                for i, task in enumerate(all_tasks, 1):
                    task['id'] = i
                
                return self._schedule_tasks_with_dates(
                    all_tasks, 
                    original_plan['goal'], 
                    original_plan['start_date'], 
                    original_plan['end_date'], 
                    original_plan.get('domain', 'AI Regenerated')
                )
            else:
                raise Exception("AI regeneration failed")
                
        except Exception as e:
            print(f"❌ AI Regeneration failed: {e}")
            return original_plan

class AIDatabase:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('ai_plans.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                plan_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE,
                completed_tasks TEXT DEFAULT '[]'
            )
        ''')
        conn.commit()
        conn.close()

    def save_plan(self, goal, plan_data):
        conn = sqlite3.connect('ai_plans.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO plans (goal, plan_data) VALUES (?, ?)',
            (goal, json.dumps(plan_data))
        )
        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return plan_id

    def get_plan(self, plan_id):
        conn = sqlite3.connect('ai_plans.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plans WHERE id = ?', (plan_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'goal': result[1],
                'plan_data': json.loads(result[2]),
                'created_at': result[3],
                'completed': bool(result[4]),
                'completed_tasks': json.loads(result[5]) if result[5] else []
            }
        return None

    def update_plan(self, plan_id, plan_data, completed_tasks):
        conn = sqlite3.connect('ai_plans.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE plans SET plan_data = ?, completed_tasks = ? WHERE id = ?',
            (json.dumps(plan_data), json.dumps(completed_tasks), plan_id)
        )
        conn.commit()
        conn.close()

# Initialize services with error handling
try:
    planner = AITaskPlanner()
    db = AIDatabase()
    print("✅ AI-powered planning services initialized")
except Exception as e:
    print(f"❌ Failed to initialize services: {e}")
    planner = None
    db = None

@app.route('/')
def home():
    return jsonify({
        "message": "AI-Powered Smart Task Planner API",
        "version": "AI-1.0",
        "features": [
            "GPT-powered intelligent planning",
            "Adaptive plan regeneration", 
            "Context-aware task generation",
            "Natural language understanding",
            "Progress-based replanning"
        ]
    })

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """Generate AI-powered plan"""
    try:
        if not planner:
            return jsonify({'error': 'AI services not available'}), 503
            
        data = request.get_json()
        goal = data.get('goal', '').strip()
        start_date = data.get('start_date', '').strip()
        end_date = data.get('end_date', '').strip()
        
        if not goal:
            return jsonify({'error': 'Goal is required'}), 400
        
        if not start_date or not end_date:
            return jsonify({'error': 'Start date and end date are required'}), 400
        
        print(f"🎯 Generating AI-powered plan for: {goal}")
        
        # Generate AI plan
        plan_data = planner.generate_ai_plan(goal, start_date, end_date)
        
        # Save to database
        plan_id = db.save_plan(goal, plan_data)
        
        return jsonify({
            'plan_id': plan_id,
            'plan': plan_data,
            'message': 'AI-powered plan generated successfully!'
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/regenerate-ai', methods=['POST'])
def regenerate_ai():
    """Regenerate plan using AI with context"""
    try:
        if not planner:
            return jsonify({'error': 'AI services not available'}), 503
            
        data = request.get_json()
        plan_id = data.get('plan_id')
        completed_tasks = data.get('completed_tasks', [])
        feedback = data.get('feedback', '')
        
        if not plan_id:
            return jsonify({'error': 'Plan ID is required'}), 400
        
        # Get existing plan
        existing_plan = db.get_plan(plan_id)
        if not existing_plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        # Regenerate with AI
        original_plan = existing_plan['plan_data']
        new_plan = planner.regenerate_with_ai(original_plan, completed_tasks, feedback)
        
        # Save as new plan
        new_plan_id = db.save_plan(original_plan['goal'], new_plan)
        
        return jsonify({
            'new_plan_id': new_plan_id,
            'plan': new_plan,
            'message': 'Plan regenerated with AI intelligence!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-progress', methods=['POST'])
def update_progress():
    """Update task completion status"""
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        completed_tasks = data.get('completed_tasks', [])
        
        if not plan_id:
            return jsonify({'error': 'Plan ID is required'}), 400
        
        existing_plan = db.get_plan(plan_id)
        if not existing_plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        db.update_plan(plan_id, existing_plan['plan_data'], completed_tasks)
        
        return jsonify({
            'message': 'Progress updated successfully!',
            'completed_tasks': completed_tasks
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plan/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    """Get specific plan"""
    plan = db.get_plan(plan_id)
    if plan:
        return jsonify(plan)
    return jsonify({'error': 'Plan not found'}), 404

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI-POWERED SMART TASK PLANNER")
    print("📍 Running on: http://localhost:5000")
    print("🤖 Powered by OpenAI GPT")
    print("=" * 60)
    
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)