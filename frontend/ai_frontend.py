from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)
BACKEND_URL = "http://localhost:5000"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanIt AI - Intelligent Task Planner</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary: #7C3AED;
            --primary-light: #8B5CF6;
            --primary-dark: #6D28D9;
            --secondary: #06D6A0;
            --accent: #FF6B6B;
            --warning: #FFD166;
            --ai-color: #10B981;
            --dark: #1E1B4B;
            --light: #F8FAFC;
            --gray: #64748B;
            --gray-light: #E2E8F0;
            --card-bg: #FFFFFF;
            --sidebar-bg: #F1F5F9;
            --gradient-primary: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%);
            --gradient-success: linear-gradient(135deg, #06D6A0 0%, #10B981 100%);
            --gradient-warning: linear-gradient(135deg, #FFD166 0%, #F59E0B 100%);
            --gradient-accent: linear-gradient(135deg, #FF6B6B 0%, #EF4444 100%);
            --gradient-ai: linear-gradient(135deg, #10B981 0%, #059669 100%);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
            --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: var(--dark);
            line-height: 1.6;
        }

        .app-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            text-align: center;
            padding: 50px 40px;
            background: var(--gradient-primary);
            border-radius: 24px;
            margin-bottom: 40px;
            color: white;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="rgba(255,255,255,0.1)"><path d="M0,70 Q250,20 500,70 T1000,70 L1000,100 L0,100 Z"/></svg>');
            background-size: cover;
        }

        .header-content {
            position: relative;
            z-index: 2;
        }

        .logo {
            font-size: 3.5em;
            font-weight: 800;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .ai-badge {
            background: var(--gradient-ai);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.4em;
            font-weight: 600;
            vertical-align: super;
        }

        .tagline {
            font-size: 1.4em;
            opacity: 0.95;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .subtagline {
            opacity: 0.8;
            font-size: 1.1em;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Main Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 30px;
            align-items: start;
        }

        /* Input Section */
        .input-section {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }

        .input-group {
            margin-bottom: 30px;
        }

        .input-label {
            display: block;
            margin-bottom: 12px;
            font-weight: 600;
            color: var(--dark);
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .input-label i {
            color: var(--primary);
        }

        .goal-input {
            width: 100%;
            padding: 20px;
            border: 2px solid var(--gray-light);
            border-radius: 16px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 140px;
            background: var(--light);
            transition: all 0.3s ease;
            line-height: 1.5;
        }

        .goal-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
            background: white;
            transform: translateY(-2px);
        }

        .timeline-inputs {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .text-input {
            width: 100%;
            padding: 16px 20px;
            border: 2px solid var(--gray-light);
            border-radius: 12px;
            font-size: 16px;
            background: var(--light);
            transition: all 0.3s ease;
            font-family: inherit;
        }

        .text-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
            background: white;
            transform: translateY(-2px);
        }

        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 25px;
        }

        .btn {
            padding: 18px 24px;
            border: none;
            border-radius: 14px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-family: inherit;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
            box-shadow: var(--shadow-md);
        }

        .btn-ai {
            background: var(--gradient-ai);
            color: white;
            box-shadow: var(--shadow-md);
        }

        .btn-secondary {
            background: var(--light);
            color: var(--dark);
            border: 2px solid var(--gray-light);
            box-shadow: var(--shadow-sm);
        }

        .btn-warning {
            background: var(--gradient-warning);
            color: var(--dark);
            box-shadow: var(--shadow-md);
        }

        .btn-success {
            background: var(--gradient-success);
            color: white;
            box-shadow: var(--shadow-md);
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }

        .btn:active {
            transform: translateY(-1px);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* AI Features */
        .ai-features {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }

        .ai-features h4 {
            color: var(--ai-color);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .ai-features ul {
            list-style: none;
            color: var(--gray);
        }

        .ai-features li {
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .ai-features li:before {
            content: '🤖';
            font-size: 0.9em;
        }

        /* Domain Examples */
        .domain-examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }

        .domain-btn {
            background: white;
            border: 2px solid var(--gray-light);
            padding: 18px 15px;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            font-size: 0.9em;
            font-weight: 500;
            color: var(--dark);
            box-shadow: var(--shadow-sm);
        }

        .domain-btn:hover {
            border-color: var(--primary);
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
            color: var(--primary);
        }

        .domain-btn i {
            font-size: 1.4em;
            margin-bottom: 8px;
            display: block;
            color: var(--primary);
        }

        /* AI Regeneration Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(30px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .modal-title {
            font-size: 1.5em;
            font-weight: 700;
            color: var(--dark);
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: var(--gray);
            transition: color 0.3s ease;
        }

        .close-btn:hover {
            color: var(--dark);
        }

        /* Results Section */
        .results-section {
            display: none;
            animation: fadeInUp 0.6s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .plan-header {
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
            margin-bottom: 30px;
            border-left: 5px solid var(--primary);
            position: relative;
            overflow: hidden;
        }

        .plan-header::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: var(--gradient-primary);
            opacity: 0.05;
            border-radius: 50%;
            transform: translate(100px, -100px);
        }

        .ai-indicator {
            background: var(--gradient-ai);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 15px;
        }

        .plan-title {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--dark);
            line-height: 1.3;
        }

        .plan-meta {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 18px;
            background: var(--light);
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            color: var(--dark);
            border: 1px solid var(--gray-light);
        }

        .meta-item i {
            color: var(--primary);
        }

        /* Tasks Grid */
        .tasks-grid {
            display: grid;
            gap: 20px;
        }

        .task-card {
            background: white;
            padding: 30px;
            border-radius: 18px;
            box-shadow: var(--shadow-lg);
            border-left: 5px solid var(--primary);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .task-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .task-card:hover::before {
            transform: scaleX(1);
        }

        .task-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
        }

        .task-card.completed {
            opacity: 0.9;
            border-left-color: var(--secondary);
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
        }

        .task-card.overdue {
            border-left-color: var(--accent);
            background: linear-gradient(135deg, #FFFFFF 0%, #FEF2F2 100%);
        }

        .task-card.regenerated {
            border-left-color: var(--ai-color);
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF9 100%);
        }

        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            gap: 20px;
        }

        .task-content {
            flex: 1;
        }

        .task-description {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            line-height: 1.4;
            color: var(--dark);
        }

        .task-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }

        .task-tag {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .tag-priority {
            background: rgba(124, 58, 237, 0.1);
            color: var(--primary-dark);
            border: 1px solid rgba(124, 58, 237, 0.2);
        }

        .tag-category {
            background: rgba(6, 214, 160, 0.1);
            color: #059669;
            border: 1px solid rgba(6, 214, 160, 0.2);
        }

        .tag-duration {
            background: rgba(255, 107, 107, 0.1);
            color: #DC2626;
            border: 1px solid rgba(255, 107, 107, 0.2);
        }

        .tag-ai {
            background: rgba(16, 185, 129, 0.1);
            color: var(--ai-color);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .task-dates {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--gray-light);
        }

        .date-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9em;
            color: var(--gray);
            font-weight: 500;
        }

        .date-item i {
            color: var(--primary);
        }

        .task-actions {
            display: flex;
            gap: 10px;
            flex-shrink: 0;
        }

        .action-btn {
            padding: 10px 18px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-complete {
            background: var(--gradient-success);
            color: white;
            box-shadow: var(--shadow-sm);
        }

        .btn-edit {
            background: var(--light);
            color: var(--gray);
            border: 1px solid var(--gray-light);
            box-shadow: var(--shadow-sm);
        }

        .btn-delete {
            background: var(--gradient-accent);
            color: white;
            box-shadow: var(--shadow-sm);
        }

        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        /* Sidebar */
        .sidebar {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
            position: sticky;
            top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .sidebar-section {
            margin-bottom: 35px;
        }

        .sidebar-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--gray-light);
        }

        .sidebar-title i {
            color: var(--primary);
        }

        .stats-grid {
            display: grid;
            gap: 15px;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px;
            background: var(--light);
            border-radius: 14px;
            border: 1px solid var(--gray-light);
            transition: all 0.3s ease;
        }

        .stat-item:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .stat-value {
            font-weight: 700;
            font-size: 1.4em;
            color: var(--primary);
        }

        .progress-ring {
            width: 70px;
            height: 70px;
        }

        .progress-bg {
            fill: none;
            stroke: var(--gray-light);
            stroke-width: 3;
        }

        .progress-fill {
            fill: none;
            stroke: var(--secondary);
            stroke-width: 3;
            stroke-linecap: round;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
            transition: stroke-dashoffset 0.5s ease;
        }

        /* Loading State */
        .loading {
            display: none;
            text-align: center;
            padding: 80px 20px;
            background: white;
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
        }

        .spinner {
            width: 60px;
            height: 60px;
            border: 4px solid var(--gray-light);
            border-left: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 25px;
        }

        .ai-spinner {
            border-left: 4px solid var(--ai-color);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading h3 {
            font-size: 1.4em;
            margin-bottom: 10px;
            color: var(--dark);
        }

        .loading p {
            color: var(--gray);
            font-size: 1.1em;
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .sidebar {
                position: static;
            }
        }

        @media (max-width: 768px) {
            .app-container {
                padding: 15px;
            }
            
            .header {
                padding: 40px 25px;
            }
            
            .logo {
                font-size: 2.8em;
            }
            
            .input-section {
                padding: 30px;
            }
            
            .timeline-inputs {
                grid-template-columns: 1fr;
            }
            
            .action-buttons {
                grid-template-columns: 1fr;
            }
            
            .domain-examples {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .task-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .task-actions {
                align-self: flex-end;
                width: 100%;
                justify-content: flex-end;
            }
            
            .plan-meta {
                flex-direction: column;
                gap: 10px;
            }
        }

        @media (max-width: 480px) {
            .domain-examples {
                grid-template-columns: 1fr;
            }
            
            .task-dates {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <div class="header">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-rocket"></i>
                    PlanIt <span class="ai-badge">AI</span>
                </div>
                <p class="tagline">AI-Powered Intelligent Task Planner</p>
                <p class="subtagline">Transform any goal into intelligent, adaptive plans with AI</p>
            </div>
        </div>

        <!-- Main Content Grid -->
        <div class="main-grid">
            <!-- Left Column - Input & Results -->
            <div class="main-content">
                <!-- Input Section -->
                <div class="input-section">
                    <div class="input-group">
                        <label class="input-label">
                            <i class="fas fa-bullseye"></i>
                            What do you want to accomplish?
                        </label>
                        <textarea 
                            class="goal-input" 
                            id="goalInput" 
                            placeholder="Describe your goal in natural language...&#10;&#10;Examples:&#10;• Learn Spanish for my trip to Spain in 3 months&#10;• Build a mobile app for task management&#10;• Start an online business selling handmade crafts&#10;• Get fit and lose 10kg by summer"
                        ></textarea>
                    </div>

                    <div class="input-group">
                        <label class="input-label">
                            <i class="fas fa-calendar-alt"></i>
                            Timeline
                        </label>
                        <div class="timeline-inputs">
                            <div>
                                <label style="display: block; margin-bottom: 8px; font-weight: 600; color: var(--dark);">Start Date</label>
                                <input type="date" class="text-input" id="startDate">
                            </div>
                            <div>
                                <label style="display: block; margin-bottom: 8px; font-weight: 600; color: var(--dark);">End Date</label>
                                <input type="date" class="text-input" id="endDate">
                            </div>
                        </div>
                    </div>

                    <div class="action-buttons">
                        <button class="btn btn-ai" id="generateBtn" onclick="generateAIPlan()">
                            <i class="fas fa-robot"></i>
                            Generate AI Plan
                        </button>
                        <button class="btn btn-secondary" onclick="openCustomTaskModal()">
                            <i class="fas fa-plus"></i>
                            Add Custom Task
                        </button>
                    </div>

                    <!-- AI Features -->
                    <div class="ai-features">
                        <h4><i class="fas fa-brain"></i> AI-Powered Features</h4>
                        <ul>
                            <li>Intelligent task breakdown based on your goal</li>
                            <li>Automatic domain detection and planning</li>
                            <li>Context-aware scheduling and dependencies</li>
                            <li>Adaptive plan regeneration based on progress</li>
                        </ul>
                    </div>

                    <!-- Quick Examples -->
                    <div class="domain-examples">
                        <div class="domain-btn" onclick="loadExample('learning')">
                            <i class="fas fa-graduation-cap"></i>
                            Learning Goal
                        </div>
                        <div class="domain-btn" onclick="loadExample('project')">
                            <i class="fas fa-briefcase"></i>
                            Project
                        </div>
                        <div class="domain-btn" onclick="loadExample('fitness')">
                            <i class="fas fa-running"></i>
                            Fitness
                        </div>
                        <div class="domain-btn" onclick="loadExample('business')">
                            <i class="fas fa-chart-line"></i>
                            Business
                        </div>
                    </div>
                </div>

                <!-- Loading State -->
                <div class="loading" id="loadingState">
                    <div class="spinner ai-spinner"></div>
                    <h3>AI is creating your intelligent plan...</h3>
                    <p>Analyzing your goal and generating optimal tasks</p>
                </div>

                <!-- Results Section -->
                <div class="results-section" id="resultsSection">
                    <!-- Plan header and tasks will be inserted here -->
                </div>
            </div>

            <!-- Right Column - Sidebar -->
            <div class="sidebar">
                <!-- Progress Overview -->
                <div class="sidebar-section">
                    <h3 class="sidebar-title">
                        <i class="fas fa-chart-pie"></i>
                        Progress Overview
                    </h3>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <span>Total Tasks</span>
                            <span class="stat-value" id="totalTasks">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Completed</span>
                            <span class="stat-value" id="completedTasks">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Remaining</span>
                            <span class="stat-value" id="remainingTasks">0</span>
                        </div>
                        <div class="stat-item">
                            <span>Overall Progress</span>
                            <div class="progress-ring">
                                <svg viewBox="0 0 36 36">
                                    <path class="progress-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                    <path class="progress-fill" id="progressFill" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- AI Actions -->
                <div class="sidebar-section">
                    <h3 class="sidebar-title">
                        <i class="fas fa-robot"></i>
                        AI Actions
                    </h3>
                    <div class="stats-grid">
                        <button class="btn btn-ai" style="width: 100%; margin-bottom: 12px;" onclick="openAIRegenerationModal()">
                            <i class="fas fa-sync-alt"></i>
                            AI Regenerate
                        </button>
                        <button class="btn btn-success" style="width: 100%; margin-bottom: 12px;" onclick="markAllComplete()">
                            <i class="fas fa-check-double"></i>
                            Mark All Complete
                        </button>
                        <button class="btn btn-secondary" style="width: 100%; margin-bottom: 12px;" onclick="exportPlan()">
                            <i class="fas fa-download"></i>
                            Export Plan
                        </button>
                        <button class="btn" style="width: 100%; background: var(--light); color: var(--gray); border: 2px solid var(--gray-light);" onclick="clearPlan()">
                            <i class="fas fa-trash"></i>
                            Clear Plan
                        </button>
                    </div>
                </div>

                <!-- AI Tips -->
                <div class="sidebar-section">
                    <h3 class="sidebar-title">
                        <i class="fas fa-lightbulb"></i>
                        AI Tips
                    </h3>
                    <div style="font-size: 0.9em; color: var(--gray); line-height: 1.6;">
                        <p style="margin-bottom: 12px;">• <strong>Be specific</strong> - AI understands detailed goals better</p>
                        <p style="margin-bottom: 12px;">• <strong>Include context</strong> - Mention constraints or preferences</p>
                        <p style="margin-bottom: 12px;">• <strong>Use AI regeneration</strong> - Adapt plans as you progress</p>
                        <p>• <strong>Provide feedback</strong> - AI learns from your adjustments</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- AI Regeneration Modal -->
    <div class="modal" id="aiRegenerationModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title"><i class="fas fa-robot"></i> AI Plan Regeneration</h3>
                <button class="close-btn" onclick="closeAIRegenerationModal()">&times;</button>
            </div>
            <div class="input-group">
                <label class="input-label">Feedback for AI (Optional)</label>
                <textarea 
                    class="text-input" 
                    id="aiFeedback" 
                    placeholder="Tell AI what to adjust...&#10;Examples:&#10;• The tasks are too difficult&#10;• I need more technical details&#10;• Make it more focused on marketing&#10;• Add more beginner-friendly steps"
                    style="min-height: 100px;"
                ></textarea>
            </div>
            <button class="btn btn-ai" style="width: 100%; margin-top: 20px;" onclick="regenerateWithAI()">
                <i class="fas fa-magic"></i>
                Regenerate with AI
            </button>
        </div>
    </div>

    <!-- Custom Task Modal -->
    <div class="modal" id="customTaskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">Add Custom Task</h3>
                <button class="close-btn" onclick="closeCustomTaskModal()">&times;</button>
            </div>
            <div class="input-group">
                <label class="input-label">Task Description</label>
                <input type="text" class="text-input" id="customTaskDescription" placeholder="What do you need to accomplish?">
            </div>
            <div class="input-group">
                <label class="input-label">Duration (days)</label>
                <input type="number" class="text-input" id="customTaskDuration" value="2" min="1" max="14">
            </div>
            <div class="input-group">
                <label class="input-label">Dependencies (optional)</label>
                <select class="text-input" id="customTaskDependencies" multiple style="height: 100px; padding: 12px;">
                    <!-- Will be populated with existing tasks -->
                </select>
                <small style="color: var(--gray); margin-top: 8px; display: block; font-size: 0.85em;">Hold Ctrl/Cmd to select multiple prerequisites</small>
            </div>
            <button class="btn btn-primary" style="width: 100%; margin-top: 25px;" onclick="addCustomTask()">
                <i class="fas fa-plus-circle"></i>
                Add to Plan
            </button>
        </div>
    </div>

    <script>
        let currentPlanId = null;
        let completedTasks = new Set();

        // Set default dates
        document.getElementById('startDate').valueAsDate = new Date();
        let endDate = new Date();
        endDate.setDate(endDate.getDate() + 30); // Default 1 month
        document.getElementById('endDate').valueAsDate = endDate;

        // Example templates
        const examples = {
            learning: "Learn Spanish for my trip to Spain in 3 months. I want to be able to have basic conversations, order food, and ask for directions. I have no prior experience with Spanish.",
            project: "Build a mobile app for task management using React Native. The app should include task creation, categories, due dates, notifications, and data synchronization across devices.",
            fitness: "Get fit and lose 10kg in 3 months. I want to build a sustainable workout routine and healthy eating habits. I currently exercise occasionally but want to be more consistent.",
            business: "Start an online business selling handmade leather goods. I need to create products, build an e-commerce website, develop marketing strategy, and handle shipping logistics."
        };

        function loadExample(type) {
            document.getElementById('goalInput').value = examples[type];
        }

        async function generateAIPlan() {
            const goal = document.getElementById('goalInput').value.trim();
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;

            if (!goal) {
                alert('Please describe your goal for AI to generate a plan.');
                return;
            }

            if (!startDate || !endDate) {
                alert('Please set both start and end dates.');
                return;
            }

            // Validate dates
            const start = new Date(startDate);
            const end = new Date(endDate);
            if (end <= start) {
                alert('End date must be after start date.');
                return;
            }

            // Show AI loading state
            document.getElementById('loadingState').style.display = 'block';
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('generateBtn').disabled = true;

            try {
                const response = await fetch('/api/generate-plan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        goal: goal,
                        start_date: startDate,
                        end_date: endDate
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    currentPlanId = data.plan_id;
                    completedTasks.clear();
                    displayPlan(data.plan);
                    showAIToast('AI plan generated successfully!');
                } else {
                    throw new Error(data.error || 'AI failed to generate plan');
                }
            } catch (error) {
                alert('Error generating AI plan: ' + error.message);
                console.error('Error:', error);
            } finally {
                document.getElementById('loadingState').style.display = 'none';
                document.getElementById('generateBtn').disabled = false;
            }
        }

        function displayPlan(plan) {
            const resultsSection = document.getElementById('resultsSection');
            
            // Clear previous content
            resultsSection.innerHTML = '';
            
            // Create plan header
            const planHeader = document.createElement('div');
            planHeader.className = 'plan-header';
            
            let aiIndicator = '';
            if (plan.ai_generated) {
                aiIndicator = `<div class="ai-indicator">
                    <i class="fas fa-robot"></i>
                    AI-Generated Plan • ${plan.domain}
                </div>`;
            }
            
            planHeader.innerHTML = `
                ${aiIndicator}
                <h2 class="plan-title">${plan.goal}</h2>
                <div class="plan-meta">
                    <div class="meta-item">
                        <i class="fas fa-play-circle"></i>
                        Start: ${formatDate(plan.start_date)}
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-flag-checkered"></i>
                        End: ${formatDate(plan.end_date)}
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-tasks"></i>
                        ${plan.total_tasks} tasks
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-calendar"></i>
                        ${plan.total_days} days total
                    </div>
                </div>
            `;
            
            // Create tasks container
            const tasksContainer = document.createElement('div');
            tasksContainer.className = 'tasks-grid';
            tasksContainer.id = 'tasksContainer';
            
            // Add tasks
            plan.tasks.forEach((task) => {
                const taskCard = document.createElement('div');
                taskCard.className = `task-card ${task.regenerated ? 'regenerated' : ''}`;
                taskCard.id = `task-${task.id}`;
                
                let aiTag = '';
                if (plan.ai_generated) {
                    aiTag = `<span class="task-tag tag-ai">
                        <i class="fas fa-brain"></i>
                        AI Suggested
                    </span>`;
                }
                
                taskCard.innerHTML = `
                    <div class="task-header">
                        <div class="task-content">
                            <div class="task-description">${task.description}</div>
                            <div class="task-meta">
                                <span class="task-tag tag-priority">
                                    <i class="fas fa-flag"></i>
                                    ${task.priority}
                                </span>
                                <span class="task-tag tag-category">
                                    <i class="fas fa-tag"></i>
                                    ${task.category}
                                </span>
                                <span class="task-tag tag-duration">
                                    <i class="fas fa-clock"></i>
                                    ${task.duration_days} day${task.duration_days > 1 ? 's' : ''}
                                </span>
                                ${aiTag}
                            </div>
                            <div class="task-dates">
                                <div class="date-item">
                                    <i class="fas fa-play-circle"></i>
                                    Start: ${formatDate(task.start_date)}
                                </div>
                                <div class="date-item">
                                    <i class="fas fa-stop-circle"></i>
                                    Due: ${formatDate(task.end_date)}
                                </div>
                            </div>
                            ${task.dependencies && task.dependencies.length > 0 ? `
                            <div style="margin-top: 15px; font-size: 0.85em; color: var(--gray); background: var(--light); padding: 10px 15px; border-radius: 10px; border-left: 3px solid var(--primary);">
                                <i class="fas fa-link"></i>
                                <strong>Prerequisites:</strong> Complete ${task.dependencies.map(dep => `Task ${dep}`).join(', ')} first
                            </div>
                            ` : ''}
                        </div>
                        <div class="task-actions">
                            <button class="action-btn btn-complete" onclick="toggleTaskComplete(${task.id})">
                                <i class="fas fa-check"></i>
                                Complete
                            </button>
                        </div>
                    </div>
                `;
                tasksContainer.appendChild(taskCard);
            });
            
            // Assemble results section
            resultsSection.appendChild(planHeader);
            resultsSection.appendChild(tasksContainer);
            
            // Show results
            resultsSection.style.display = 'block';
            updateProgress();
        }

        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
        }

        async function toggleTaskComplete(taskId) {
            const taskCard = document.getElementById(`task-${taskId}`);
            
            if (completedTasks.has(taskId)) {
                completedTasks.delete(taskId);
                taskCard.classList.remove('completed');
            } else {
                completedTasks.add(taskId);
                taskCard.classList.add('completed');
            }
            
            // Update progress in backend
            if (currentPlanId) {
                try {
                    await fetch('/api/update-progress', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            plan_id: currentPlanId,
                            completed_tasks: Array.from(completedTasks).map(id => ({ id }))
                        })
                    });
                } catch (error) {
                    console.error('Error updating progress:', error);
                }
            }
            
            updateProgress();
        }

        function updateProgress() {
            const totalTasks = document.querySelectorAll('.task-card').length;
            const completedCount = completedTasks.size;
            const progress = totalTasks > 0 ? Math.round((completedCount / totalTasks) * 100) : 0;
            
            document.getElementById('totalTasks').textContent = totalTasks;
            document.getElementById('completedTasks').textContent = completedCount;
            document.getElementById('remainingTasks').textContent = totalTasks - completedCount;
            
            // Update progress ring
            const circumference = 2 * Math.PI * 15.9155;
            const offset = circumference - (progress / 100) * circumference;
            document.getElementById('progressFill').style.strokeDasharray = `${circumference} ${circumference}`;
            document.getElementById('progressFill').style.strokeDashoffset = offset;
        }

        function openAIRegenerationModal() {
            if (!currentPlanId) {
                alert('Please generate a plan first.');
                return;
            }

            document.getElementById('aiRegenerationModal').style.display = 'flex';
        }

        function closeAIRegenerationModal() {
            document.getElementById('aiRegenerationModal').style.display = 'none';
            document.getElementById('aiFeedback').value = '';
        }

        async function regenerateWithAI() {
            const feedback = document.getElementById('aiFeedback').value.trim();

            // Show AI loading
            document.getElementById('loadingState').style.display = 'block';
            closeAIRegenerationModal();

            try {
                const response = await fetch('/api/regenerate-ai', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        plan_id: currentPlanId,
                        completed_tasks: Array.from(completedTasks).map(id => ({ id })),
                        feedback: feedback
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    currentPlanId = data.new_plan_id;
                    displayPlan(data.plan);
                    showAIToast('Plan regenerated with AI intelligence!');
                } else {
                    throw new Error(data.error || 'AI regeneration failed');
                }
            } catch (error) {
                alert('Error regenerating with AI: ' + error.message);
                console.error('Error:', error);
            } finally {
                document.getElementById('loadingState').style.display = 'none';
            }
        }

        function showAIToast(message) {
            // Create toast notification
            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--gradient-ai);
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                box-shadow: var(--shadow-lg);
                z-index: 1001;
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
            `;
            toast.innerHTML = `<i class="fas fa-robot"></i> ${message}`;
            document.body.appendChild(toast);

            setTimeout(() => {
                toast.remove();
            }, 3000);
        }

        function openCustomTaskModal() {
            if (!currentPlanId) {
                alert('Please generate a plan first.');
                return;
            }

            const dependenciesSelect = document.getElementById('customTaskDependencies');
            dependenciesSelect.innerHTML = '';
            
            // Populate with existing tasks
            document.querySelectorAll('.task-card').forEach(taskCard => {
                const taskId = taskCard.id.replace('task-', '');
                const taskDescription = taskCard.querySelector('.task-description').textContent;
                const option = document.createElement('option');
                option.value = taskId;
                option.textContent = `Task ${taskId}: ${taskDescription.substring(0, 40)}${taskDescription.length > 40 ? '...' : ''}`;
                dependenciesSelect.appendChild(option);
            });

            document.getElementById('customTaskModal').style.display = 'flex';
        }

        function closeCustomTaskModal() {
            document.getElementById('customTaskModal').style.display = 'none';
            document.getElementById('customTaskDescription').value = '';
            document.getElementById('customTaskDuration').value = '2';
        }

        async function addCustomTask() {
            const description = document.getElementById('customTaskDescription').value.trim();
            const duration = parseInt(document.getElementById('customTaskDuration').value);
            const dependencies = Array.from(document.getElementById('customTaskDependencies').selectedOptions)
                .map(option => parseInt(option.value));

            if (!description) {
                alert('Please enter a task description.');
                return;
            }

            if (duration < 1 || duration > 14) {
                alert('Duration should be between 1 and 14 days.');
                return;
            }

            try {
                const response = await fetch('/api/add-custom-task', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        plan_id: currentPlanId,
                        task_description: description,
                        duration_days: duration,
                        dependencies: dependencies
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    displayPlan(data.plan);
                    closeCustomTaskModal();
                    alert('Task added successfully!');
                } else {
                    throw new Error(data.error || 'Failed to add task');
                }
            } catch (error) {
                alert('Error adding task: ' + error.message);
                console.error('Error:', error);
            }
        }

        function markAllComplete() {
            document.querySelectorAll('.task-card').forEach(taskCard => {
                const taskId = parseInt(taskCard.id.replace('task-', ''));
                completedTasks.add(taskId);
                taskCard.classList.add('completed');
            });
            updateProgress();
        }

        function exportPlan() {
            alert('Export feature coming soon! Your AI-generated plan is automatically saved.');
        }

        function clearPlan() {
            if (confirm('Are you sure you want to clear your current plan?')) {
                document.getElementById('resultsSection').style.display = 'none';
                document.getElementById('goalInput').value = '';
                currentPlanId = null;
                completedTasks.clear();
                updateProgress();
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_CONTENT

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.get_json()
        goal = data.get('goal')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not all([goal, start_date, end_date]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Send request to AI backend
        backend_response = requests.post(
            f"{BACKEND_URL}/api/generate-plan",
            json={
                'goal': goal,
                'start_date': start_date,
                'end_date': end_date
            },
            timeout=60  # Longer timeout for AI processing
        )
        
        if backend_response.status_code == 200:
            backend_data = backend_response.json()
            return jsonify({'plan_id': backend_data['plan_id'], 'plan': backend_data['plan']})
        else:
            error_msg = backend_response.json().get('error', 'AI backend service unavailable')
            return jsonify({'error': error_msg}), 503
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI backend connection failed: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/regenerate-ai', methods=['POST'])
def regenerate_ai():
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        completed_tasks = data.get('completed_tasks', [])
        feedback = data.get('feedback', '')
        
        if not plan_id:
            return jsonify({'error': 'Plan ID is required'}), 400
        
        backend_response = requests.post(
            f"{BACKEND_URL}/api/regenerate-ai",
            json={
                'plan_id': plan_id,
                'completed_tasks': completed_tasks,
                'feedback': feedback
            },
            timeout=60
        )
        
        if backend_response.status_code == 200:
            backend_data = backend_response.json()
            return jsonify(backend_data)
        else:
            error_msg = backend_response.json().get('error', 'AI regeneration failed')
            return jsonify({'error': error_msg}), 503
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI backend connection failed: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/add-custom-task', methods=['POST'])
def add_custom_task():
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        task_description = data.get('task_description')
        duration_days = data.get('duration_days', 1)
        dependencies = data.get('dependencies', [])
        
        if not all([plan_id, task_description]):
            return jsonify({'error': 'Plan ID and task description are required'}), 400
        
        backend_response = requests.post(
            f"{BACKEND_URL}/api/add-custom-task",
            json={
                'plan_id': plan_id,
                'task_description': task_description,
                'duration_days': duration_days,
                'dependencies': dependencies
            },
            timeout=30
        )
        
        if backend_response.status_code == 200:
            backend_data = backend_response.json()
            return jsonify(backend_data)
        else:
            error_msg = backend_response.json().get('error', 'Backend service unavailable')
            return jsonify({'error': error_msg}), 503
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Backend connection failed: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/update-progress', methods=['POST'])
def update_progress():
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        completed_tasks = data.get('completed_tasks', [])
        
        if not plan_id:
            return jsonify({'error': 'Plan ID is required'}), 400
        
        backend_response = requests.post(
            f"{BACKEND_URL}/api/update-progress",
            json={
                'plan_id': plan_id,
                'completed_tasks': completed_tasks
            },
            timeout=30
        )
        
        if backend_response.status_code == 200:
            return jsonify({'message': 'Progress updated successfully'})
        else:
            error_msg = backend_response.json().get('error', 'Backend service unavailable')
            return jsonify({'error': error_msg}), 503
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Backend connection failed: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 PlanIt AI Frontend Starting...")
    print("📍 Running on: http://localhost:8000")
    print("🔗 AI Backend URL:", BACKEND_URL)
    print("=" * 50)
    print("🤖 AI-POWERED FEATURES:")
    print("   • GPT-powered intelligent planning")
    print("   • Adaptive plan regeneration")
    print("   • Natural language understanding")
    print("   • Context-aware task generation")
    print("   • Progress-based AI adjustments")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8000, debug=True)