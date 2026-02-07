import React from 'react';
import Card from './Card';

const ContentPanel = ({ title, children, className = '' }) => {
  return (
    <Card variant="strong" className={`${className}`}>
      <div className="space-y-6">
        {title && (
          <div className="border-b border-white/10 pb-4">
            <h1 className="text-3xl font-bold text-white mb-2">{title}</h1>
            <div className="h-1 w-16 bg-gradient-to-r from-teal-400 to-teal-600 rounded-full"></div>
          </div>
        )}
        
        <div className="prose prose-invert max-w-none">
          <div className="text-gray-300 leading-relaxed space-y-4">
            {children}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ContentPanel;
