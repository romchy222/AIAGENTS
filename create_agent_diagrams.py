#!/usr/bin/env python3
"""
Script to create a visual diagram showing the frontend-backend agent connections
in the BolashakChat system.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_agent_architecture_diagram():
    """Create a comprehensive diagram showing the frontend-backend agent architecture."""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors
    frontend_color = '#3B82F6'  # Blue
    api_color = '#10B981'       # Green
    agent_color = '#8B5CF6'     # Purple
    ai_color = '#F59E0B'        # Orange
    db_color = '#EF4444'        # Red
    
    # Title
    ax.text(5, 9.5, 'BolashakChat: Архитектура Frontend-Backend Agent Connections', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Frontend Layer
    frontend_box = FancyBboxPatch((0.5, 7.5), 2, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=frontend_color, 
                                  edgecolor='black', 
                                  alpha=0.7)
    ax.add_patch(frontend_box)
    ax.text(1.5, 8.6, 'FRONTEND', ha='center', va='center', fontweight='bold', color='white')
    ax.text(1.5, 8.2, '• Agent Cards', ha='center', va='center', color='white', fontsize=10)
    ax.text(1.5, 7.9, '• Chat Interface', ha='center', va='center', color='white', fontsize=10)
    ax.text(1.5, 7.6, '• JS Routing', ha='center', va='center', color='white', fontsize=10)
    
    # API Gateway
    api_box = FancyBboxPatch((4, 7.5), 2, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor=api_color, 
                             edgecolor='black', 
                             alpha=0.7)
    ax.add_patch(api_box)
    ax.text(5, 8.6, 'API GATEWAY', ha='center', va='center', fontweight='bold', color='white')
    ax.text(5, 8.2, '/api/chat', ha='center', va='center', color='white', fontsize=10)
    ax.text(5, 7.9, 'views.py', ha='center', va='center', color='white', fontsize=10)
    ax.text(5, 7.6, 'Agent Routing', ha='center', va='center', color='white', fontsize=10)
    
    # Agent Router
    router_box = FancyBboxPatch((7.5, 7.5), 2, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=agent_color, 
                                edgecolor='black', 
                                alpha=0.7)
    ax.add_patch(router_box)
    ax.text(8.5, 8.6, 'AGENT ROUTER', ha='center', va='center', fontweight='bold', color='white')
    ax.text(8.5, 8.2, 'AgentRouter', ha='center', va='center', color='white', fontsize=10)
    ax.text(8.5, 7.9, 'Confidence', ha='center', va='center', color='white', fontsize=10)
    ax.text(8.5, 7.6, 'Scoring', ha='center', va='center', color='white', fontsize=10)
    
    # Individual Agents
    agents = [
        ('AI-Abitur', 'Поступление', 0.5, 5.5),
        ('KadrAI', 'Кадры', 2.5, 5.5),
        ('UniNav', 'Учеба', 4.5, 5.5),
        ('CareerNav', 'Карьера', 6.5, 5.5),
        ('UniRoom', 'Общежитие', 8.5, 5.5)
    ]
    
    for name, desc, x, y in agents:
        agent_box = FancyBboxPatch((x-0.4, y-0.4), 0.8, 0.8, 
                                   boxstyle="round,pad=0.05", 
                                   facecolor=agent_color, 
                                   edgecolor='black', 
                                   alpha=0.8)
        ax.add_patch(agent_box)
        ax.text(x, y+0.15, name, ha='center', va='center', fontweight='bold', color='white', fontsize=9)
        ax.text(x, y-0.15, desc, ha='center', va='center', color='white', fontsize=8)
    
    # AI Processing Layer
    ai_box = FancyBboxPatch((3.5, 3.5), 3, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=ai_color, 
                            edgecolor='black', 
                            alpha=0.7)
    ax.add_patch(ai_box)
    ax.text(5, 4.2, 'AI PROCESSING', ha='center', va='center', fontweight='bold', color='white')
    ax.text(5, 3.8, 'Mistral AI Client', ha='center', va='center', color='white', fontsize=10)
    ax.text(5, 3.6, 'Specialized Prompts', ha='center', va='center', color='white', fontsize=10)
    
    # Database Layer
    db_box = FancyBboxPatch((1, 1.5), 8, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=db_color, 
                            edgecolor='black', 
                            alpha=0.7)
    ax.add_patch(db_box)
    ax.text(5, 2.2, 'DATABASE & ANALYTICS', ha='center', va='center', fontweight='bold', color='white')
    ax.text(2.5, 1.8, 'UserQuery', ha='center', va='center', color='white', fontsize=10)
    ax.text(5, 1.8, 'Agent Tracking', ha='center', va='center', color='white', fontsize=10)
    ax.text(7.5, 1.8, 'Analytics Dashboard', ha='center', va='center', color='white', fontsize=10)
    
    # Arrows - Frontend to API
    arrow1 = ConnectionPatch((2.5, 8.25), (4, 8.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="black", ec="black")
    ax.add_patch(arrow1)
    ax.text(3.25, 8.5, 'POST /api/chat', ha='center', va='center', fontsize=8)
    
    # Arrows - API to Router
    arrow2 = ConnectionPatch((6, 8.25), (7.5, 8.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="black", ec="black")
    ax.add_patch(arrow2)
    ax.text(6.75, 8.5, 'route_message()', ha='center', va='center', fontsize=8)
    
    # Arrows - Router to Agents
    for _, _, x, y in agents:
        arrow = ConnectionPatch((8.5, 7.5), (x, y+0.4), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5, 
                               mutation_scale=15, fc="gray", ec="gray", alpha=0.7)
        ax.add_patch(arrow)
    
    # Arrows - Agents to AI
    for _, _, x, y in agents:
        arrow = ConnectionPatch((x, y-0.4), (5, 4.5), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5, 
                               mutation_scale=15, fc="orange", ec="orange", alpha=0.7)
        ax.add_patch(arrow)
    
    # Arrow - AI to DB
    arrow_db = ConnectionPatch((5, 3.5), (5, 2.5), "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5, 
                              mutation_scale=20, fc="red", ec="red")
    ax.add_patch(arrow_db)
    ax.text(5.5, 3, 'Store Results', ha='center', va='center', fontsize=8, rotation=-90)
    
    # Data Flow Indicators
    ax.text(0.2, 6.5, 'USER\nINTERACTION', ha='center', va='center', 
            fontweight='bold', fontsize=10, rotation=90, color='blue')
    ax.text(9.8, 6.5, 'INTELLIGENT\nROUTING', ha='center', va='center', 
            fontweight='bold', fontsize=10, rotation=-90, color='purple')
    
    # Legend
    legend_y = 0.8
    ax.text(0.5, legend_y, 'Flow Legend:', fontweight='bold', fontsize=10)
    ax.text(0.5, legend_y-0.2, '1. User selects agent or sends message', fontsize=9)
    ax.text(0.5, legend_y-0.4, '2. Frontend sends request to /api/chat', fontsize=9)
    ax.text(0.5, legend_y-0.6, '3. AgentRouter analyzes and routes to best agent', fontsize=9)
    ax.text(5.5, legend_y-0.2, '4. Agent processes with specialized prompt', fontsize=9)
    ax.text(5.5, legend_y-0.4, '5. AI generates contextual response', fontsize=9)
    ax.text(5.5, legend_y-0.6, '6. Results stored for analytics', fontsize=9)
    
    plt.tight_layout()
    return fig

def create_agent_details_diagram():
    """Create a detailed diagram showing agent specializations and connections."""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Детализация AI-Агентов и их Специализации', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Agent details
    agents_detail = [
        {
            'name': 'AI-Abitur',
            'type': 'ai_abitur',
            'color': '#FF6B6B',
            'pos': (1.5, 7.5),
            'keywords': ['поступление', 'абитуриент', 'документы', 'экзамен'],
            'description': 'Помощь при поступлении'
        },
        {
            'name': 'KadrAI',
            'type': 'kadrai',
            'color': '#4ECDC4',
            'pos': (5, 7.5),
            'keywords': ['кадры', 'отпуск', 'перевод', 'приказ'],
            'description': 'Кадровые процессы'
        },
        {
            'name': 'UniNav',
            'type': 'uninav',
            'color': '#45B7D1',
            'pos': (8.5, 7.5),
            'keywords': ['расписание', 'учёба', 'заявление', 'деканат'],
            'description': 'Учебные процессы'
        },
        {
            'name': 'CareerNavigator',
            'type': 'career_navigator',
            'color': '#F7DC6F',
            'pos': (3, 4.5),
            'keywords': ['работа', 'трудоустройство', 'вакансии', 'резюме'],
            'description': 'Карьера и трудоустройство'
        },
        {
            'name': 'UniRoom',
            'type': 'uniroom',
            'color': '#BB8FCE',
            'pos': (7, 4.5),
            'keywords': ['общежитие', 'заселение', 'переселение', 'бытовые'],
            'description': 'Студенческое общежитие'
        }
    ]
    
    # Draw agent boxes with details
    for agent in agents_detail:
        x, y = agent['pos']
        
        # Main agent box
        agent_box = FancyBboxPatch((x-0.8, y-0.8), 1.6, 1.6, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=agent['color'], 
                                   edgecolor='black', 
                                   alpha=0.8)
        ax.add_patch(agent_box)
        
        # Agent name
        ax.text(x, y+0.4, agent['name'], ha='center', va='center', 
                fontweight='bold', fontsize=11, color='white')
        
        # Agent type
        ax.text(x, y+0.1, f"({agent['type']})", ha='center', va='center', 
                fontsize=9, color='white', style='italic')
        
        # Description
        ax.text(x, y-0.2, agent['description'], ha='center', va='center', 
                fontsize=9, color='white')
        
        # Keywords box
        keywords_text = ', '.join(agent['keywords'][:2]) + '...'
        ax.text(x, y-0.5, keywords_text, ha='center', va='center', 
                fontsize=8, color='white', style='italic')
    
    # Central routing logic
    router_box = FancyBboxPatch((4.2, 1.5), 1.6, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#2C3E50', 
                                edgecolor='black', 
                                alpha=0.9)
    ax.add_patch(router_box)
    ax.text(5, 2.1, 'AgentRouter', ha='center', va='center', 
            fontweight='bold', color='white', fontsize=12)
    ax.text(5, 1.8, 'Confidence Scoring', ha='center', va='center', 
            color='white', fontsize=10)
    ax.text(5, 1.6, 'Best Match Selection', ha='center', va='center', 
            color='white', fontsize=10)
    
    # Arrows from router to agents
    for agent in agents_detail:
        x, y = agent['pos']
        arrow = ConnectionPatch((5, 2.5), (x, y-0.8), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5, 
                               mutation_scale=15, fc="gray", ec="gray", alpha=0.6)
        ax.add_patch(arrow)
    
    # Confidence scoring example
    ax.text(1, 2.5, 'Пример оценки уверенности:', fontweight='bold', fontsize=11)
    ax.text(1, 2.2, '"Как поступить?" → AI-Abitur (1.0)', fontsize=10)
    ax.text(1, 1.9, '"Где стипендия?" → CareerNav (0.6)', fontsize=10)
    ax.text(1, 1.6, '"Расписание?" → UniNav (0.8)', fontsize=10)
    ax.text(1, 1.3, '"Общие вопросы" → Auto-select (0.3)', fontsize=10)
    
    plt.tight_layout()
    return fig

def save_diagrams():
    """Save both diagrams as PNG files."""
    
    # Create architecture diagram
    fig1 = create_agent_architecture_diagram()
    fig1.savefig('/home/runner/work/AIAGENTS/AIAGENTS/frontend_backend_architecture.png', 
                 dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    
    # Create agent details diagram
    fig2 = create_agent_details_diagram()
    fig2.savefig('/home/runner/work/AIAGENTS/AIAGENTS/agent_details_diagram.png', 
                 dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    
    print("Diagrams saved successfully!")
    print("1. frontend_backend_architecture.png - Overall system architecture")
    print("2. agent_details_diagram.png - Detailed agent specializations")

if __name__ == "__main__":
    save_diagrams()