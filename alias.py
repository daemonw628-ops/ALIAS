"""
ALIAS - Advanced Learning Intelligence Assistant System
The Ultimate AI Companion with ALL Features Combined

Voice + Text + Study + Work + Creative + Personal + Tech + Fun
Everything in one powerful AI assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
import datetime
import threading
import time
import webbrowser
import subprocess
import asyncio
import logging
from typing import Optional, List, Dict, Any
import requests
from urllib.parse import quote
import re
import random

# Voice components (optional - will work without if not available)
try:
    import speech_recognition as sr
    import pyttsx3
    import pygame
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Voice features not available - install speech dependencies for full ALIAS experience")

# AI backends (try to import what's available)
AI_BACKENDS = {}

# Try Hugging Face Transformers for local AI
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    AI_BACKENDS['transformers'] = True
except ImportError:
    AI_BACKENDS['transformers'] = False

# Try requests for free online APIs
AI_BACKENDS['online'] = True

# Try to import our custom Free AI Engine
try:
    from ai_engine import FreeAIEngine as CustomFreeAIEngine
    AI_BACKENDS['custom_free'] = True
except ImportError:
    AI_BACKENDS['custom_free'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FreeAIEngine:
    """Free AI Engine with multiple backends"""
    
    def __init__(self):
        self.backends = []
        self.patterns = self.load_pattern_responses()
        self.custom_engine = None
        self.initialize_backends()
        
    def initialize_backends(self):
        """Initialize available free AI backends"""
        # Try our custom Free AI Engine FIRST (best option)
        if AI_BACKENDS.get('custom_free'):
            try:
                self.custom_engine = CustomFreeAIEngine()
                self.backends.append('custom_free')
                logger.info("Custom Free AI Engine loaded - truly free AI active!")
            except Exception as e:
                logger.warning(f"Custom engine failed: {e}")
        
        # Try local Hugging Face models
        if AI_BACKENDS.get('transformers'):
            try:
                self.hf_generator = pipeline("text-generation", model="microsoft/DialoGPT-medium")
                self.backends.append('huggingface_local')
                logger.info("Local HF model loaded")
            except Exception as e:
                logger.warning(f"HF model failed: {e}")
        
        # Try Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                self.backends.append('ollama')
                logger.info("Ollama detected")
        except:
            pass
        
        # Free online APIs
        self.backends.extend(['huggingface_api', 'groq_free'])
        
        # Always have pattern fallback
        self.backends.append('patterns')
        
        self.current_backend = self.backends[0]
        logger.info(f"Using backend: {self.current_backend}")
    
    def load_pattern_responses(self):
        """Intelligent pattern responses"""
        return {
            r'\b(hello|hi|hey|greetings)\b': [
                "Hello! I'm ALIAS, your AI assistant. How may I help you today?",
                "Greetings! ALIAS at your service. What can I assist you with?",
            ],
            r'\b(study|learn|homework|explain|teach)\b': [
                "I'd be happy to help you study! What subject or concept would you like to explore?",
                "Learning is excellent! What topic would you like me to explain?",
            ],
            r'\b(math|calculate|solve|equation)\b': [
                "I can help with mathematical problems! Please share the specific equation or concept.",
                "Mathematics is one of my strengths. What calculation can I assist with?",
            ],
            r'\b(code|program|debug|python|javascript)\b': [
                "I can assist with programming! What language and what's the challenge?",
                "Coding help is available! Please share your code or describe the issue.",
            ],
            r'\b(write|story|creative|poem|essay)\b': [
                "I love helping with creative writing! What type of project are you working on?",
                "Creative writing is fantastic! Tell me about your story or creative project.",
            ],
            r'\b(work|job|email|business|professional)\b': [
                "I can help with professional tasks! What work-related challenge can I assist with?",
                "Productivity assistance is available! What business task needs attention?",
            ],
            r'\b(time|date|weather|today)\b': [
                f"The current time is {datetime.datetime.now().strftime('%I:%M %p')} on {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
            ],
            r'\b(joke|fun|game|entertain)\b': [
                "Here's a joke: Why don't scientists trust atoms? Because they make up everything!",
                "Fun time! What do you call a bear with no teeth? A gummy bear!",
            ],
            r'.*': [
                "I understand you're asking about that topic. Could you be more specific about what you need help with?",
                "That's an interesting question! I can provide assistance. What specifically do you need?",
            ]
        }
    
    def get_response(self, message, mode="Assistant", subject="General"):
        """Get AI response using best available backend"""
        for backend in self.backends:
            try:
                if backend == 'custom_free':
                    return self.get_custom_engine_response(message, mode, subject)
                elif backend == 'huggingface_local':
                    return self.get_huggingface_response(message, mode)
                elif backend == 'ollama':
                    return self.get_ollama_response(message, mode)
                elif backend == 'huggingface_api':
                    return self.get_huggingface_api_response(message, mode)
                elif backend == 'groq_free':
                    return self.get_groq_response(message, mode)
                elif backend == 'patterns':
                    return self.get_pattern_response(message, mode)
            except Exception as e:
                logger.warning(f"Backend {backend} failed: {e}")
                continue
        
        return "I apologize, but I'm having trouble generating a response. Please try again."
    
    def get_custom_engine_response(self, message, mode, subject):
        """Our custom free AI engine"""
        if self.custom_engine is None:
            raise Exception("Custom engine not available")
        return self.custom_engine.get_response(message, mode, subject)
    
    def get_huggingface_response(self, message, mode):
        """Local HF model response"""
        if not hasattr(self, 'hf_generator'):
            raise Exception("HF model not available")
        
        prompt = self.create_mode_prompt(message, mode)
        response = self.hf_generator(prompt, max_length=150, temperature=0.7, do_sample=True, pad_token_id=50256)
        return response[0]['generated_text'][len(prompt):].strip()
    
    def get_ollama_response(self, message, mode):
        """Ollama local response"""
        prompt = self.create_mode_prompt(message, mode)
        response = requests.post("http://localhost:11434/api/generate",
                               json={"model": "llama2", "prompt": prompt, "stream": False}, timeout=30)
        if response.status_code == 200:
            return response.json()['response']
        raise Exception("Ollama failed")
    
    def get_huggingface_api_response(self, message, mode):
        """Free HF Inference API"""
        # Using free models that don't require API keys
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        response = requests.post(API_URL, json={"inputs": message}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'] if result else self.get_pattern_response(message, mode)
        raise Exception("HF API failed")
    
    def get_groq_response(self, message, mode):
        """Groq free tier (if available)"""
        # Groq offers free API tier - could be implemented
        raise Exception("Groq not configured")
    
    def get_pattern_response(self, message, mode):
        """Pattern matching response"""
        message_lower = message.lower()
        
        for pattern, responses in self.patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                response = random.choice(responses)
                
                # Add mode context
                if mode == "Study":
                    response += " I'm in study mode, so I can help explain concepts, solve problems, or create practice questions."
                elif mode == "Work":
                    response += " I'm in professional mode, ready to assist with business tasks and productivity."
                elif mode == "Creative":
                    response += " I'm in creative mode, perfect for writing, brainstorming, and artistic projects."
                elif mode == "Tech":
                    response += " I'm in technical mode, ready to help with programming and tech questions."
                elif mode == "Personal":
                    response += " I'm in personal assistant mode, here to help with life planning and goals."
                elif mode == "Fun":
                    response += " I'm in fun mode, ready to entertain and have casual conversations!"
                
                return response
        
        return random.choice(self.patterns[r'.*'])
    
    def create_mode_prompt(self, message, mode):
        """Create mode-specific prompts"""
        contexts = {
            "Assistant": "You are ALIAS, a helpful AI assistant. Respond helpfully and professionally.",
            "Study": "You are ALIAS in tutoring mode. Provide clear educational explanations.",
            "Work": "You are ALIAS in professional mode. Help with business tasks.",
            "Creative": "You are ALIAS in creative mode. Assist with writing and creative projects.",
            "Personal": "You are ALIAS in personal assistant mode. Help with life planning.",
            "Tech": "You are ALIAS in technical mode. Provide programming assistance.",
            "Fun": "You are ALIAS in entertainment mode. Be engaging and helpful."
        }
        
        context = contexts.get(mode, contexts["Assistant"])
        return f"{context}\n\nUser: {message}\nALIAS:"


class ALIAS:
    """
    The Ultimate FREE ALIAS - All AI Features with Zero Cost
    Voice + Text + Multi-Mode + Study + Work + Everything
    """
    
    def __init__(self, start_mode="Assistant"):
        """Initialize FREE ALIAS with all capabilities"""
        self.root = tk.Tk()
        
        # Initialize free AI engine
        self.ai_engine = FreeAIEngine()
        
        # Core configuration
        self.conversation_history = []
        self.current_mode = start_mode
        self.current_subject = "General"
        
        # Session tracking
        self.session_start = datetime.datetime.now()
        self.messages_sent = 0
        self.voice_enabled = VOICE_AVAILABLE
        self.is_listening = False
        
        # Voice components
        if VOICE_AVAILABLE:
            self.setup_voice_components()
        
        # All modes and capabilities
        self.modes = {
            "Assistant": "General AI assistant for anything",
            "Study": "Academic tutoring and learning",
            "Work": "Professional productivity and tasks", 
            "Creative": "Writing and creative projects",
            "Personal": "Life management and planning",
            "Tech": "Programming and technical help",
            "Fun": "Entertainment and casual chat",
            "Voice": "Voice interaction mode"
        }
        
        # Setup GUI (must come after modes are defined)
        self.setup_gui()
        
        # Load settings and initialize
        self.load_settings()
        
        # Set the starting mode after GUI is created
        if start_mode != "Assistant":
            self.mode_var.set(start_mode)
            self.mode_desc_label.config(text=self.modes[start_mode])
            self.mode_label.config(text=f"Mode: {start_mode}")
        
        self.show_welcome()
    
    def setup_voice_components(self):
        """Initialize voice recognition and TTS"""
        try:
            if VOICE_AVAILABLE:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                self.tts_engine = pyttsx3.init()
                
                # Configure TTS
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Try to find a male voice for ALIAS
                    for voice in voices:
                        if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 0.8)
                
                # Initialize pygame for audio
                pygame.mixer.init()
                
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                logger.info("Voice components initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing voice: {e}")
            self.voice_enabled = False
    
    def setup_gui(self):
        """Create the ultimate FREE ALIAS interface"""
        self.root.title("A.L.I.A.S.")
        self.root.geometry("600x700")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # ALIAS-style theme
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a', 
            'bg_panel': '#2d2d2d',
            'accent_blue': '#00d4ff',
            'accent_gold': '#ffd700',
            'accent_green': '#00ff88',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_dim': '#888888'
        }
        
        # Create the interface
        self.create_header()
        self.create_main_interface()
        self.create_status_bar()
        
        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.send_message())
        self.root.bind('<Control-l>', lambda e: self.toggle_voice_listening())
        self.root.bind('<Control-m>', lambda e: self.cycle_mode())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Alt-F4>', lambda e: self.on_closing())
        
        # Start with welcome
        self.add_ALIAS_message("FREE ALIAS is online and ready to assist you with anything!")
        self.add_ALIAS_message(f"Using {self.ai_engine.current_backend.replace('_', ' ').title()} AI backend - completely free!")
        self.add_ALIAS_message("I can help with study, work, creativity, personal tasks, and more - no API costs!")
        if VOICE_AVAILABLE:
            self.add_ALIAS_message("Voice features are available. Press Ctrl+L to toggle listening.")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show_welcome(self):
        """Show welcome message"""
        backend_name = self.ai_engine.current_backend.replace('_', ' ').title()
        self.add_ALIAS_message(f"FREE ALIAS Online - Using {backend_name} backend")
        self.add_ALIAS_message("Advanced AI assistance with zero costs - for everyone, everywhere!")
        if VOICE_AVAILABLE:
            self.add_ALIAS_message("Voice features ready. Use wake words: 'ALIAS', 'Hey ALIAS', 'OK ALIAS'")
    
    def create_header(self):
        """Create the ALIAS header with all controls"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Center everything
        center_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        center_frame.pack(expand=True, fill='both')
        
        # Create circular avatar using canvas
        avatar_frame = tk.Frame(center_frame, bg=self.colors['bg_secondary'])
        avatar_frame.pack(side='left', padx=20)
        
        canvas = tk.Canvas(avatar_frame, width=50, height=50, 
                          bg=self.colors['bg_secondary'], 
                          highlightthickness=0)
        canvas.pack(pady=15)
        
        # Draw circle
        canvas.create_oval(5, 5, 45, 45, 
                          fill=self.colors['accent_green'], 
                          outline=self.colors['accent_blue'], 
                          width=2)
        
        # ALIAS title
        title_label = tk.Label(center_frame, text="A.L.I.A.S.", 
                              font=('Arial', 18, 'bold'), 
                              fg=self.colors['accent_green'], 
                              bg=self.colors['bg_secondary'])
        title_label.pack(side='left', pady=15)
        
        # Right side - minimal controls
        right_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        right_frame.pack(side='right', padx=20)
        
        controls_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'])
        controls_frame.pack(pady=15)
        
        # Mode selector (compact)
        self.mode_var = tk.StringVar(value=self.current_mode)
        self.mode_combo = ttk.Combobox(controls_frame, textvariable=self.mode_var,
                                      values=list(self.modes.keys()),
                                      width=10, state='readonly',
                                      font=('Arial', 9))
        self.mode_combo.pack(side='left', padx=5)
        self.mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # Clear button
        tk.Button(controls_frame, text="Clear", command=self.clear_chat,
                 bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                 font=('Arial', 9), padx=10).pack(side='left', padx=5)
    
    def create_main_interface(self):
        """Create the main chat and tools interface"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Center - Chat area
        self.create_chat_area(main_frame)
        
        # Bottom - Input area
        self.create_input_area(main_frame)
    
    def create_sidebar(self, parent):
        """Create comprehensive sidebar with all tools"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['bg_panel'], width=280)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar title
        tk.Label(sidebar_frame, text="ALIAS Capabilities", 
                font=('Arial', 14, 'bold'), 
                fg=self.colors['accent_gold'], 
                bg=self.colors['bg_panel']).pack(pady=(15, 20))
        
        # Create scrollable frame for tools
        canvas = tk.Canvas(sidebar_frame, bg=self.colors['bg_panel'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_panel'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add all capabilities
        self.create_all_tools(scrollable_frame)
        
        # Session stats at bottom
        self.create_session_stats(sidebar_frame)
    
    def create_all_tools(self, parent):
        """Create all tool categories"""
        # Study Tools
        self.create_tool_section(parent, "Study & Learning", [
            ("Explain Concept", lambda: self.set_prompt("Explain this concept: ")),
            ("Solve Problem", lambda: self.set_prompt("Help me solve: ")),
            ("Check Answer", lambda: self.set_prompt("Is this correct? ")),
            ("Create Quiz", lambda: self.set_prompt(f"Create a quiz on {self.current_subject}")),
            ("Summarize", lambda: self.set_prompt("Summarize this: ")),
            ("Study Tips", lambda: self.set_prompt(f"Study tips for {self.current_subject}"))
        ])
        
        # Work & Productivity
        self.create_tool_section(parent, "Work & Productivity", [
            ("Write Email", lambda: self.set_prompt("Write a professional email about: ")),
            ("Analyze Data", lambda: self.set_prompt("Analyze this data: ")),
            ("Create Plan", lambda: self.set_prompt("Create a plan for: ")),
            ("Set Goals", lambda: self.set_prompt("Help me set goals for: ")),
            ("Time Management", lambda: self.set_prompt("Time management tips for: ")),
            ("Write Report", lambda: self.set_prompt("Help me write a report on: "))
        ])
        
        # Creative & Writing
        self.create_tool_section(parent, "Creative & Writing", [
            ("Write Story", lambda: self.set_prompt("Help me write a story about: ")),
            ("Creative Ideas", lambda: self.set_prompt("Creative ideas for: ")),
            ("Edit Text", lambda: self.set_prompt("Edit and improve this: ")),
            ("Character Dev", lambda: self.set_prompt("Develop a character who: ")),
            ("Song Lyrics", lambda: self.set_prompt("Write lyrics about: ")),
            ("Brainstorm", lambda: self.set_prompt("Brainstorm ideas for: "))
        ])
        
        # Tech & Programming
        self.create_tool_section(parent, "Tech & Programming", [
            ("Code Help", lambda: self.set_prompt("Help with this code: ")),
            ("Debug Issue", lambda: self.set_prompt("Debug this problem: ")),
            ("Tool Recommend", lambda: self.set_prompt("Recommend tools for: ")),
            ("Learn Tech", lambda: self.set_prompt("How to learn: ")),
            ("Architecture", lambda: self.set_prompt("Design architecture for: ")),
            ("Code Review", lambda: self.set_prompt("Review this code: "))
        ])
        
        # Personal & Life
        self.create_tool_section(parent, "Personal & Life", [
            ("Life Planning", lambda: self.set_prompt("Help me plan: ")),
            ("Budget Help", lambda: self.set_prompt("Budget advice for: ")),
            ("Meal Planning", lambda: self.set_prompt("Plan meals for: ")),
            ("Fitness Plan", lambda: self.set_prompt("Fitness plan for: ")),
            ("Wellness Tips", lambda: self.set_prompt("Wellness tips for: ")),
            ("Schedule Help", lambda: self.set_prompt("Organize schedule for: "))
        ])
        
        # Quick Actions
        self.create_tool_section(parent, "⚡ Quick Actions", [
            ("Web Search", self.web_search),
            ("Weather", lambda: self.send_direct_message("What's the weather?")),
            ("News", lambda: self.send_direct_message("Latest news headlines")),
            ("Time", self.get_time),
            ("Open Folder", self.open_folder),
            ("System Info", lambda: self.send_direct_message("System information"))
        ])
        
        # Fun & Entertainment
        self.create_tool_section(parent, "Fun & Entertainment", [
            ("Tell Joke", lambda: self.send_direct_message("Tell me a joke")),
            ("Random Fact", lambda: self.send_direct_message("Random fun fact")),
            ("Movie Rec", lambda: self.set_prompt("Recommend movies about: ")),
            ("Book Rec", lambda: self.set_prompt("Recommend books about: ")),
            ("Game Ideas", lambda: self.set_prompt("Game ideas for: ")),
            ("Entertain Me", lambda: self.send_direct_message("Entertain me"))
        ])
    
    def create_tool_section(self, parent, title, tools):
        """Create a collapsible tool section"""
        section_frame = tk.LabelFrame(parent, text=title, 
                                     fg=self.colors['text_primary'], 
                                     bg=self.colors['bg_panel'],
                                     font=('Arial', 10, 'bold'))
        section_frame.pack(fill='x', padx=10, pady=5)
        
        for text, command in tools:
            btn = tk.Button(section_frame, text=text, command=command,
                           bg=self.colors['bg_secondary'], 
                           fg=self.colors['text_secondary'],
                           font=('Arial', 9), width=25,
                           relief='flat', pady=3,
                           activebackground=self.colors['accent_blue'],
                           activeforeground='black')
            btn.pack(pady=1, padx=5, fill='x')
    
    def create_session_stats(self, parent):
        """Create session statistics display"""
        stats_frame = tk.LabelFrame(parent, text="Session Stats", 
                                   fg=self.colors['text_primary'], 
                                   bg=self.colors['bg_panel'],
                                   font=('Arial', 10, 'bold'))
        stats_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        self.session_time_label = tk.Label(stats_frame, text="Time: 0:00", 
                                          fg=self.colors['text_secondary'], 
                                          bg=self.colors['bg_panel'],
                                          font=('Arial', 9))
        self.session_time_label.pack(anchor='w', padx=5, pady=2)
        
        self.messages_label = tk.Label(stats_frame, text="Messages: 0", 
                                      fg=self.colors['text_secondary'], 
                                      bg=self.colors['bg_panel'],
                                      font=('Arial', 9))
        self.messages_label.pack(anchor='w', padx=5, pady=2)
        
        self.mode_label = tk.Label(stats_frame, text=f"Mode: {self.current_mode}", 
                                  fg=self.colors['accent_blue'], 
                                  bg=self.colors['bg_panel'],
                                  font=('Arial', 9, 'bold'))
        self.mode_label.pack(anchor='w', padx=5, pady=2)
        
        if VOICE_AVAILABLE:
            self.voice_status_label = tk.Label(stats_frame, text="Voice: Ready", 
                                              fg=self.colors['accent_gold'], 
                                              bg=self.colors['bg_panel'],
                                              font=('Arial', 9))
            self.voice_status_label.pack(anchor='w', padx=5, pady=2)
        
        # Start stats timer
        self.update_session_stats()
    
    def create_chat_area(self, parent):
        """Create the main chat interface"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        chat_frame.pack(side='left', fill='both', expand=True)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=('Consolas', 11),
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent_blue']
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0, 10))
        
        # Configure text tags for ALIAS styling
        self.chat_display.tag_configure('user', 
                                       foreground=self.colors['accent_blue'], 
                                       font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('ALIAS', 
                                       foreground=self.colors['accent_green'], 
                                       font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('system', 
                                       foreground=self.colors['text_dim'], 
                                       font=('Consolas', 10, 'italic'))
        self.chat_display.tag_configure('timestamp', 
                                       foreground='#666666', 
                                       font=('Consolas', 9))
        self.chat_display.tag_configure('mode', 
                                       foreground='#ff6b35', 
                                       font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure('voice', 
                                       foreground='#00ff88', 
                                       font=('Consolas', 10, 'italic'))
    
    def create_input_area(self, parent):
        """Create the input area with voice integration"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=1)
        input_frame.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=4,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief='flat',
            bd=10
        )
        self.input_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.input_text.bind('<Return>', lambda e: self.send_message_on_enter(e))
        
        # Button panel
        button_panel = tk.Frame(input_frame, bg=self.colors['bg_panel'])
        button_panel.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Send button
        self.send_button = tk.Button(button_panel, text="Send\n(Enter)", 
                                    command=self.send_message,
                                    bg=self.colors['accent_blue'], fg='black',
                                    font=('Arial', 11, 'bold'),
                                    width=12, height=2,
                                    relief='flat')
        self.send_button.pack(pady=(0, 5))
        
        # Voice button (if available)
        if VOICE_AVAILABLE:
            self.voice_input_button = tk.Button(button_panel, text="Voice\nInput", 
                                               command=self.voice_input_once,
                                               bg=self.colors['accent_gold'], fg='black',
                                               font=('Arial', 10, 'bold'),
                                               width=12,
                                               relief='flat')
            self.voice_input_button.pack(pady=(0, 5))
        
        # Mode quick switch
        tk.Button(button_panel, text="Mode\n(Ctrl+M)", 
                 command=self.cycle_mode,
                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                 font=('Arial', 9),
                 width=12,
                 relief='flat').pack()
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = tk.Label(self.root, text="FREE ALIAS Online - Zero API costs!", 
                                  relief=tk.SUNKEN, anchor='w',
                                  bg=self.colors['bg_secondary'], 
                                  fg=self.colors['accent_green'], 
                                  font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
    
    def send_message_on_enter(self, event):
        """Send message when Enter is pressed (Shift+Enter for new line)"""
        if event.state & 0x1:  # Shift key is pressed
            return  # Allow default behavior (new line)
        else:
            self.send_message()
            return 'break'  # Prevent default Enter behavior
    
    def send_message(self):
        """Send message to ALIAS"""
        message = self.input_text.get(1.0, tk.END).strip()
        if not message:
            return
        
        self.input_text.delete(1.0, tk.END)
        self.add_user_message(message)
        
        # Show ALIAS is thinking
        self.status_bar.config(text="ALIAS is processing your request...")
        self.send_button.config(state='disabled', text="Processing...")
        
        # Process in background
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process message with FREE ALIAS AI"""
        try:
            response = self.ai_engine.get_response(message, self.current_mode, self.current_subject)
            
            self.root.after(0, lambda: self.add_ALIAS_response(response))
            self.root.after(0, lambda: self.status_bar.config(text="FREE ALIAS Online - Zero API costs!"))
            self.root.after(0, lambda: self.send_button.config(state='normal', text="Send\n(Enter)"))
            
            # Speak response if voice is enabled
            if VOICE_AVAILABLE and response:
                threading.Thread(target=lambda: self.speak_if_available(response), daemon=True).start()
            
            self.messages_sent += 1
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            self.root.after(0, lambda: self.add_ALIAS_response(error_msg))
            self.root.after(0, lambda: self.status_bar.config(text="Error occurred"))
            self.root.after(0, lambda: self.send_button.config(state='normal', text="Send\n(Enter)"))
    
    def add_user_message(self, message):
        """Add user message to chat"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "You: ", 'user')
        self.chat_display.insert(tk.END, f"{message}\n\n", 'normal')
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def add_ALIAS_response(self, response):
        """Add ALIAS response to chat"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "FREE ALIAS: ", 'ALIAS')
        self.chat_display.insert(tk.END, f"{response}\n\n", 'normal')
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def add_ALIAS_message(self, message):
        """Add ALIAS system message"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"{message}\n\n", 'system')
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def speak_if_available(self, text):
        """Speak text if TTS is available"""
        try:
            if VOICE_AVAILABLE and hasattr(self, 'tts_engine'):
                # Limit length for speech
                if len(text) > 200:
                    text = text[:200] + "..."
                
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def toggle_voice_listening(self):
        """Toggle continuous voice listening"""
        if not VOICE_AVAILABLE:
            messagebox.showinfo("Voice Not Available", "Voice features require speech_recognition, pyttsx3, and pyaudio packages.")
            return
        
        if not self.is_listening:
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def start_voice_listening(self):
        """Start continuous voice listening"""
        self.is_listening = True
        self.voice_button.config(text="Stop Listening", bg='#ff4444')
        self.voice_status_label.config(text="Voice: Listening")
        
        # Start listening in background
        threading.Thread(target=self.voice_listening_loop, daemon=True).start()
    
    def stop_voice_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_button.config(text="Start Listening", bg=self.colors['accent_blue'])
        self.voice_status_label.config(text="Voice: Ready")
    
    def voice_listening_loop(self):
        """Main voice listening loop"""
        wake_words = ["ALIAS", "hey ALIAS", "ok ALIAS"]
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for wake word
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # Check for wake word
                    for wake_word in wake_words:
                        if wake_word in text:
                            self.root.after(0, lambda: self.add_ALIAS_message("Wake word detected, listening for command..."))
                            
                            # Listen for command
                            with self.microphone as source:
                                command_audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            
                            try:
                                command = self.recognizer.recognize_google(command_audio)
                                self.root.after(0, lambda c=command: self.process_voice_command(c))
                            except sr.UnknownValueError:
                                self.root.after(0, lambda: self.add_ALIAS_message("I didn't catch that command, sir."))
                            break
                            
                except sr.UnknownValueError:
                    pass  # No speech detected
                    
            except sr.WaitTimeoutError:
                pass  # Normal timeout
            except Exception as e:
                logger.error(f"Voice listening error: {e}")
                time.sleep(1)
    
    def process_voice_command(self, command):
        """Process a voice command"""
        self.add_user_message(f"{command}")
        
        # Set to voice mode for appropriate response length
        original_mode = self.current_mode
        self.current_mode = "Voice"
        
        # Process the command
        self.send_button.config(state='disabled', text="Processing...")
        threading.Thread(target=self.process_message, args=(command,), daemon=True).start()
        
        # Restore original mode
        self.current_mode = original_mode
    
    def voice_input_once(self):
        """Single voice input"""
        if not VOICE_AVAILABLE:
            messagebox.showinfo("Voice Not Available", "Voice features require additional packages.")
            return
        
        self.voice_input_button.config(text="Listening...", state='disabled')
        
        def listen():
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                text = self.recognizer.recognize_google(audio)
                self.root.after(0, lambda: self.input_text.insert(tk.END, text))
                
            except sr.WaitTimeoutError:
                self.root.after(0, lambda: self.add_ALIAS_message("No speech detected."))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.add_ALIAS_message("Could not understand the audio."))
            except Exception as e:
                self.root.after(0, lambda: self.add_ALIAS_message(f"Voice input error: {e}"))
            finally:
                self.root.after(0, lambda: self.voice_input_button.config(text="Voice\nInput", state='normal'))
        
        threading.Thread(target=listen, daemon=True).start()
    
    def on_mode_change(self, event=None):
        """Handle mode change"""
        new_mode = self.mode_var.get()
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self.mode_desc_label.config(text=self.modes[new_mode])
            self.mode_label.config(text=f"Mode: {new_mode}")
            
            self.add_ALIAS_message(f"Switched to {new_mode} mode: {self.modes[new_mode]}")
            self.save_settings()
    
    def on_subject_change(self, event=None):
        """Handle subject change"""
        new_subject = self.subject_var.get()
        if new_subject != self.current_subject:
            self.current_subject = new_subject
            self.add_ALIAS_message(f"Subject specialization: {new_subject}")
            self.save_settings()
    
    def cycle_mode(self):
        """Cycle through modes quickly"""
        modes = list(self.modes.keys())
        current_index = modes.index(self.current_mode)
        next_index = (current_index + 1) % len(modes)
        self.mode_var.set(modes[next_index])
        self.on_mode_change()
    
    def set_prompt(self, prompt):
        """Set a prompt in the input field"""
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, prompt)
        self.input_text.focus()
        self.input_text.mark_set(tk.INSERT, tk.END)
    
    def send_direct_message(self, message):
        """Send a message directly"""
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, message)
        self.send_message()
    
    def clear_chat(self):
        """Clear the chat history"""
        if messagebox.askyesno("Clear Chat", "Clear conversation history?", 
                              parent=self.root):
            self.chat_display.config(state='normal')
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state='disabled')
            
            self.conversation_history.clear()
            self.add_ALIAS_message("Conversation history cleared. How may I assist you?")
    
    def save_conversation(self):
        """Save conversation to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save ALIAS Conversation"
            )
            if filename:
                content = self.chat_display.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"ALIAS Conversation - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(content)
                self.add_ALIAS_message(f"Conversation saved to {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save conversation: {e}")
    
    def update_session_stats(self):
        """Update session statistics"""
        if hasattr(self, 'session_time_label'):
            elapsed = datetime.datetime.now() - self.session_start
            hours = elapsed.seconds // 3600
            minutes = (elapsed.seconds % 3600) // 60
            
            self.session_time_label.config(text=f"Time: {hours}:{minutes:02d}")
            self.messages_label.config(text=f"Messages: {self.messages_sent}")
        
        self.root.after(60000, self.update_session_stats)
    
    # Quick action implementations
    def web_search(self):
        """Open web search"""
        query = tk.simpledialog.askstring("Web Search", "What would you like to search for?")
        if query:
            webbrowser.open(f"https://www.google.com/search?q={quote(query)}")
            self.add_ALIAS_message(f"Opened web search for: {query}")
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        self.add_ALIAS_message(f"Current time: {current_time}")
        self.speak_if_available(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
    
    def open_folder(self):
        """Open file explorer"""
        try:
            subprocess.Popen('explorer')
            self.add_ALIAS_message("File Explorer opened")
        except Exception as e:
            self.add_ALIAS_message(f"Error opening File Explorer: {e}")
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("FREE ALIAS Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.colors['bg_primary'])
        settings_window.transient(self.root)
        
        tk.Label(settings_window, text="FREE ALIAS Configuration", 
                font=('Arial', 16, 'bold'), 
                fg=self.colors['accent_green'], 
                bg=self.colors['bg_primary']).pack(pady=20)
        
        # AI Backend section
        backend_frame = tk.LabelFrame(settings_window, text="AI Backend Status", 
                                     fg=self.colors['text_primary'], 
                                     bg=self.colors['bg_primary'])
        backend_frame.pack(fill='x', padx=20, pady=10)
        
        current_backend = self.ai_engine.current_backend.replace('_', ' ').title()
        tk.Label(backend_frame, text=f"Current Backend: {current_backend}", 
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_blue'], 
                bg=self.colors['bg_primary']).pack(anchor='w', padx=5, pady=5)
        
        available_backends = ", ".join([b.replace('_', ' ').title() for b in self.ai_engine.backends])
        tk.Label(backend_frame, text=f"Available: {available_backends}", 
                fg=self.colors['text_secondary'], 
                bg=self.colors['bg_primary']).pack(anchor='w', padx=5, pady=5)
        
        tk.Label(backend_frame, text="All backends are completely free!", 
                font=('Arial', 10, 'italic'),
                fg=self.colors['accent_gold'], 
                bg=self.colors['bg_primary']).pack(anchor='w', padx=5, pady=5)
        
        # Enhancement instructions
        enhance_frame = tk.LabelFrame(settings_window, text="Enhance AI Performance (Optional)", 
                                     fg=self.colors['text_primary'], 
                                     bg=self.colors['bg_primary'])
        enhance_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        instructions = [
            "🚀 For Better AI Responses:",
            "",
            "• Install Ollama: https://ollama.ai",
            "  Then run: ollama pull llama2",
            "",
            "• Install Transformers: pip install transformers torch",
            "",
            "• All options remain completely FREE!"
        ]
        
        for instruction in instructions:
            tk.Label(enhance_frame, text=instruction, 
                    font=('Arial', 10), 
                    fg=self.colors['text_primary'], 
                    bg=self.colors['bg_primary'],
                    anchor='w').pack(anchor='w', padx=10, pady=2)
        
        # Voice settings
        if VOICE_AVAILABLE:
            voice_frame = tk.LabelFrame(settings_window, text="Voice Configuration", 
                                       fg=self.colors['text_primary'], 
                                       bg=self.colors['bg_primary'])
            voice_frame.pack(fill='x', padx=20, pady=10)
            
            tk.Button(voice_frame, text="Test Microphone", 
                     command=self.test_microphone,
                     bg=self.colors['accent_gold'], fg='black',
                     font=('Arial', 10)).pack(pady=5)
            
            tk.Button(voice_frame, text="� Test Speech", 
                     command=lambda: self.speak_if_available("FREE ALIAS voice test successful"),
                     bg=self.colors['accent_gold'], fg='black',
                     font=('Arial', 10)).pack(pady=5)
    
    def test_microphone(self):
        """Test microphone functionality"""
        if not VOICE_AVAILABLE:
            messagebox.showinfo("Voice Not Available", "Voice features require additional packages.")
            return
        
        self.add_ALIAS_message("Testing microphone... Please speak now.")
        
        def test():
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                
                text = self.recognizer.recognize_google(audio)
                self.root.after(0, lambda: self.add_ALIAS_message(f"Microphone test successful! You said: '{text}'"))
                
            except sr.WaitTimeoutError:
                self.root.after(0, lambda: self.add_ALIAS_message("No speech detected during test."))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.add_ALIAS_message("Speech was unintelligible."))
            except Exception as e:
                self.root.after(0, lambda: self.add_ALIAS_message(f"Microphone test failed: {e}"))
        
        threading.Thread(target=test, daemon=True).start()
    
    def show_help(self):
        """Show ALIAS help"""
        help_window = tk.Toplevel(self.root)
        help_window.title("ALIAS Help")
        help_window.geometry("700x600")
        help_window.configure(bg=self.colors['bg_primary'])
        
        help_text = scrolledtext.ScrolledText(help_window, 
                                             font=('Consolas', 10),
                                             bg=self.colors['bg_secondary'], 
                                             fg=self.colors['text_primary'],
                                             wrap=tk.WORD)
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        help_content = """
FREE ALIAS - JUST A RATHER VERY INTELLIGENT SYSTEM

OVERVIEW:
FREE ALIAS is your ultimate AI companion with zero costs! It combines voice 
interaction, advanced tutoring, professional assistance, creative support, 
and personal management - all completely free.

AI BACKENDS:
• Pattern Matching: Built-in intelligent responses (always works)
• Ollama: Local LLMs like Llama2 (install from ollama.ai)
• Transformers: Local AI models (pip install transformers torch)
• Free APIs: Hugging Face and other free services
• Auto-Fallback: Uses best available backend automatically

KEYBOARD SHORTCUTS:
• Ctrl+Enter: Send message
• Ctrl+L: Toggle voice listening
• Ctrl+M: Cycle through modes
• F1: Show this help

MODES:
• Assistant: General AI assistance for any task
• Study: Academic tutoring with subject specialization
• Work: Professional productivity and business tasks
• Creative: Writing, brainstorming, and artistic projects
• Personal: Life management, wellness, and planning
• Tech: Programming, debugging, and technical support
• Fun: Entertainment, jokes, and casual conversation

VOICE FEATURES:
• Wake Words: "ALIAS", "Hey ALIAS", "OK ALIAS"
• Continuous Listening: Press Ctrl+L or the voice button
• Single Voice Input: Use the voice input button
• Text-to-Speech: ALIAS speaks responses when voice is active

CAPABILITIES:
Study & Learning:
- Subject-specific tutoring across all academic areas
- Problem solving with step-by-step explanations
- Quiz generation and knowledge testing
- Study tips and learning strategies

Work & Productivity:
- Professional email composition
- Project planning and management
- Data analysis assistance
- Goal setting and time management

Creative & Writing:
- Story and content creation
- Brainstorming and ideation
- Text editing and improvement
- Creative project guidance

Tech & Programming:
- Code debugging and optimization
- Architecture design assistance
- Technical documentation
- Learning new technologies

Personal & Life:
- Life planning and goal setting
- Budget and financial advice
- Health and wellness guidance
- Daily organization

Fun & Entertainment:
- Jokes and humor
- Game recommendations
- Casual conversation
- Entertainment suggestions

SETUP OPTIONS:
1. Basic: Just run FREE ALIAS (works immediately!)
2. Enhanced: Install Ollama for better AI responses
3. Advanced: Add voice features with speech packages
4. Premium: All features with local AI models

COST: $0.00 - Always and forever FREE!

FREE ALIAS makes advanced AI assistance available to everyone, 
everywhere, with zero barriers and zero costs.
        """
        
        help_text.insert(1.0, help_content)
        help_text.config(state='disabled')
    
    def load_settings(self):
        """Load ALIAS settings"""
        try:
            if os.path.exists('ALIAS_settings.json'):
                with open('ALIAS_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.current_mode = settings.get('mode', 'Assistant')
                    self.current_subject = settings.get('subject', 'General')
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save ALIAS settings"""
        try:
            settings = {
                'mode': self.current_mode,
                'subject': self.current_subject
            }
            with open('ALIAS_settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        self.save_settings()
        if self.is_listening:
            self.stop_voice_listening()
        self.root.destroy()
    
    def run(self):
        """Start ALIAS"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("ALIAS interrupted by user")
        except Exception as e:
            logger.error(f"ALIAS error: {e}")
        finally:
            logger.info("ALIAS shutdown complete")


def main():
    """Main entry point for ALIAS"""
    import sys
    
    try:
        # Check for required imports
        try:
            import tkinter.simpledialog
        except ImportError:
            pass
        
        # Parse command line arguments for starting mode
        start_mode = "Assistant"  # Default
        if len(sys.argv) > 1:
            mode_arg = sys.argv[1].title()
            valid_modes = ["Assistant", "Study", "Work", "Creative", "Personal", "Tech", "Fun"]
            if mode_arg in valid_modes:
                start_mode = mode_arg
            else:
                print(f"Invalid mode: {sys.argv[1]}")
                print(f"Valid modes: {', '.join(valid_modes)}")
                print("Starting in Assistant mode...")
        
        # Initialize and run ALIAS
        app = ALIAS(start_mode=start_mode)
        app.run()
        
    except Exception as e:
        print(f"Error starting ALIAS: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
