'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { useAuth } from '@/hooks/useAuth';
import { Bot } from 'lucide-react';
import apiClient from '@/lib/api';
import { ChatInterface } from '@/features/assistant';

export default function AssistantPage() {
  useAuth(true);
  const [conversationId, setConversationId] = useState<string | undefined>();

  const handleSendMessage = async (message: string): Promise<string> => {
    try {
      const response = await apiClient.chatWithAssistant(message, conversationId);
      
      // Store conversation ID for subsequent messages
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }
      
      return response.message;
    } catch (error: any) {
      console.error('Failed to send message:', error);
      throw new Error(
        error.response?.data?.detail || 'Failed to send message. Please try again.'
      );
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Bot className="mr-3 text-primary" size={32} />
            AI Career Assistant
          </h1>
          <p className="text-gray-600">Get personalized career advice and job search tips</p>
        </div>

        <Card className="h-[600px]">
          <ChatInterface onSendMessage={handleSendMessage} />
        </Card>
      </div>
    </DashboardLayout>
  );
}

