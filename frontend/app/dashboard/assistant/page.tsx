'use client';

import { useState, useRef, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useAuth } from '@/hooks/useAuth';
import { Message } from '@/types';
import { Send, Bot, User as UserIcon } from 'lucide-react';
import apiClient from '@/lib/api';

export default function AssistantPage() {
  useAuth(true);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI career assistant. I can help you with resume tips, interview preparation, career advice, and answer questions about jobs. How can I assist you today?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await apiClient.sendMessage(input);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      // Mock response for demo
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: getMockResponse(input),
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQuestions = [
    'How can I improve my resume?',
    'What are common interview questions?',
    'How do I negotiate salary?',
    'Tips for career change?',
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 flex items-center">
            <Bot className="mr-3 text-primary" size={32} />
            AI Career Assistant
          </h1>
          <p className="text-white">Get personalized career advice and job search tips</p>
        </div>

        <Card className="h-[600px] flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`flex items-start space-x-3 max-w-[80%] ${
                    message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user' ? 'bg-primary' : 'bg-gray-200'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <UserIcon className="text-white" size={18} />
                    ) : (
                      <Bot className="text-gray-600" size={18} />
                    )}
                  </div>
                  <div
                    className={`rounded-lg px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-line">{message.content}</p>
                    <p className="text-xs mt-1 opacity-70">
                      {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                    <Bot className="text-gray-600" size={18} />
                  </div>
                  <div className="bg-gray-100 rounded-lg px-4 py-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Questions */}
          {messages.length === 1 && (
            <div className="px-6 pb-4">
              <p className="text-sm text-gray-600 mb-2">Suggested questions:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((question) => (
                  <Button
                    key={question}
                    variant="outline"
                    size="sm"
                    onClick={() => setInput(question)}
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <form onSubmit={handleSendMessage} className="border-t border-gray-200 p-4">
            <div className="flex space-x-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1"
                disabled={isLoading}
              />
              <Button type="submit" variant="primary" disabled={!input.trim() || isLoading}>
                <Send size={18} />
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </DashboardLayout>
  );
}

function getMockResponse(question: string): string {
  const lowerQuestion = question.toLowerCase();

  if (lowerQuestion.includes('resume')) {
    return 'Here are some tips to improve your resume:\n\n1. Keep it concise (1-2 pages)\n2. Use action verbs (achieved, developed, implemented)\n3. Quantify your achievements with numbers\n4. Tailor it to each job application\n5. Include relevant keywords from the job description\n6. Proofread for any errors\n\nWould you like specific advice for any section of your resume?';
  }

  if (lowerQuestion.includes('interview')) {
    return 'Common interview questions include:\n\n1. Tell me about yourself\n2. Why do you want this job?\n3. What are your strengths and weaknesses?\n4. Where do you see yourself in 5 years?\n5. Describe a challenging situation and how you handled it\n\nFor each question, prepare specific examples using the STAR method (Situation, Task, Action, Result). Would you like help preparing for a specific question?';
  }

  if (lowerQuestion.includes('salary') || lowerQuestion.includes('negotiate')) {
    return 'Salary negotiation tips:\n\n1. Research market rates for your role and location\n2. Know your worth based on experience and skills\n3. Wait for the employer to make the first offer\n4. Express enthusiasm for the role before discussing salary\n5. Provide a range rather than a specific number\n6. Consider the entire compensation package (benefits, equity, etc.)\n7. Be professional and confident\n\nWhat specific aspect of salary negotiation would you like to discuss?';
  }

  if (lowerQuestion.includes('career change')) {
    return 'Making a career change can be exciting! Here\'s how to approach it:\n\n1. Identify transferable skills from your current role\n2. Research your target industry and required skills\n3. Consider taking courses or certifications\n4. Network with people in your target field\n5. Craft a compelling story about why you\'re changing careers\n6. Start with a lateral move if needed\n7. Update your resume to highlight relevant experience\n\nWhat field are you considering transitioning into?';
  }

  return 'That\'s a great question! I can help you with:\n\n• Resume and cover letter tips\n• Interview preparation\n• Career development advice\n• Job search strategies\n• Salary negotiation\n• Professional networking\n\nCould you provide more details about what you\'d like to know?';
}

