import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SectionBlock from './components/SectionBlock';
import ContentPanel from './components/ContentPanel';
import Card from './components/Card';

const App = () => {
  const [activeNavItem, setActiveNavItem] = useState('home');
  const [activeSection, setActiveSection] = useState('overview');

  const sections = [
    {
      id: 'overview',
      title: 'Overview',
      description: 'Introduction to the Dictionary API',
    },
    {
      id: 'authentication',
      title: 'Authentication',
      description: 'How to authenticate your requests',
    },
    {
      id: 'endpoints',
      title: 'Endpoints',
      description: 'Available API endpoints and methods',
    },
    {
      id: 'word-lookup',
      title: 'Word Lookup',
      description: 'Look up French or English words',
    },
    {
      id: 'personalization',
      title: 'Personalization',
      description: 'Context-aware vocabulary engine',
    },
    {
      id: 'examples',
      title: 'Code Examples',
      description: 'Sample code snippets and use cases',
    },
  ];

  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <>
            <p className="text-lg text-gray-300 mb-6">
              Welcome to the Dictionary Project API documentation. This comprehensive guide will help you integrate our powerful French-English dictionary service into your applications.
            </p>
            
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white mt-8 mb-4">Features</h2>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="text-teal-400 mr-3">•</span>
                  <span><strong className="text-white">Context-Aware Lookups:</strong> Get personalized word definitions based on user interests and learning style</span>
                </li>
                <li className="flex items-start">
                  <span className="text-teal-400 mr-3">•</span>
                  <span><strong className="text-white">CEFR Level Detection:</strong> Automatic difficulty level assessment (A1-C2)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-teal-400 mr-3">•</span>
                  <span><strong className="text-white">Usage Examples:</strong> Real-world French sentence examples for each word</span>
                </li>
                <li className="flex items-start">
                  <span className="text-teal-400 mr-3">•</span>
                  <span><strong className="text-white">Personalized Explanations:</strong> AI-generated explanations tailored to user interests</span>
                </li>
              </ul>
            </div>
          </>
        );
      
      case 'authentication':
        return (
          <>
            <p className="text-lg text-gray-300 mb-6">
              All API requests require authentication using an API key. Include your key in the request headers.
            </p>
            
            <Card variant="subtle" className="my-6">
              <pre className="text-sm text-gray-300 overflow-x-auto">
{`curl -X POST https://api.dictionary.com/v1/lookup \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"word": "bonjour"}'`}
              </pre>
            </Card>
          </>
        );
      
      case 'endpoints':
        return (
          <>
            <h2 className="text-2xl font-bold text-white mt-8 mb-4">Available Endpoints</h2>
            <div className="space-y-6">
              <Card variant="subtle">
                <h3 className="text-xl font-semibold text-white mb-2">POST /v1/lookup</h3>
                <p className="text-gray-400 mb-4">Look up a word and get personalized definitions, examples, and context.</p>
                <div className="space-y-2">
                  <p className="text-sm text-gray-500"><strong>Request Body:</strong></p>
                  <pre className="text-xs bg-black/30 p-3 rounded text-gray-300">
{`{
  "word": "bonjour",
  "user_profile": {
    "level": "B1",
    "interests": ["French culture", "Travel"]
  }
}`}
                  </pre>
                </div>
              </Card>
            </div>
          </>
        );
      
      case 'word-lookup':
        return (
          <>
            <p className="text-lg text-gray-300 mb-6">
              The word lookup endpoint provides comprehensive information about French and English words, including definitions, usage examples, and personalized context.
            </p>
            
            <h2 className="text-2xl font-bold text-white mt-8 mb-4">Response Format</h2>
            <Card variant="subtle" className="my-6">
              <pre className="text-sm text-gray-300 overflow-x-auto">
{`{
  "input_word": "bonjour",
  "selected_interest": "French culture",
  "conversation_fr": "Bonjour! Comment allez-vous?",
  "personalized_explanation": "...",
  "usages_fr": ["...", "...", "..."],
  "cefr_level": "A1",
  "part_of_speech": "interjection"
}`}
              </pre>
            </Card>
          </>
        );
      
      case 'personalization':
        return (
          <>
            <p className="text-lg text-gray-300 mb-6">
              Our Context-Aware Vocabulary Engine personalizes content based on user profiles, interests, and learning styles.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
              <Card variant="subtle">
                <h3 className="text-lg font-semibold text-white mb-2">Interest-Based Context</h3>
                <p className="text-sm text-gray-400">
                  Words are explained using analogies and examples from the user's selected interests.
                </p>
              </Card>
              <Card variant="subtle">
                <h3 className="text-lg font-semibold text-white mb-2">Learning Style</h3>
                <p className="text-sm text-gray-400">
                  Content tone adapts to academic or fun learning preferences.
                </p>
              </Card>
            </div>
          </>
        );
      
      case 'examples':
        return (
          <>
            <h2 className="text-2xl font-bold text-white mt-8 mb-4">JavaScript Example</h2>
            <Card variant="subtle" className="my-6">
              <pre className="text-sm text-gray-300 overflow-x-auto">
{`async function lookupWord(word, apiKey) {
  const response = await fetch('https://api.dictionary.com/v1/lookup', {
    method: 'POST',
    headers: {
      'Authorization': \`Bearer \${apiKey}\`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ word }),
  });
  
  return await response.json();
}

// Usage
const result = await lookupWord('bonjour', 'your-api-key');
console.log(result.personalized_explanation);`}
              </pre>
            </Card>
          </>
        );
      
      default:
        return <p className="text-gray-400">Select a section to view content.</p>;
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar activeItem={activeNavItem} onNavClick={setActiveNavItem} />
      
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Left Sidebar - Section Cards */}
          <aside className="lg:col-span-1">
            <SectionBlock
              title="Documentation"
              sections={sections}
              activeSection={activeSection}
              onSectionClick={setActiveSection}
            />
          </aside>

          {/* Right Content Panel */}
          <main className="lg:col-span-3">
            <ContentPanel title={sections.find(s => s.id === activeSection)?.title || 'Documentation'}>
              {renderContent()}
            </ContentPanel>
          </main>
        </div>
      </div>
    </div>
  );
};

export default App;
