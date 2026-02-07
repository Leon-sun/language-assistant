import React from 'react';
import Card from './Card';

const SectionBlock = ({ 
  title, 
  sections = [], 
  activeSection, 
  onSectionClick 
}) => {
  return (
    <div className="space-y-4">
      {title && (
        <h2 className="text-white font-semibold text-sm uppercase tracking-wider mb-4 px-2">
          {title}
        </h2>
      )}
      
      <div className="space-y-2">
        {sections.map((section) => (
          <Card
            key={section.id}
            variant={activeSection === section.id ? 'strong' : 'subtle'}
            hover={true}
            onClick={() => onSectionClick && onSectionClick(section.id)}
            className={`
              ${activeSection === section.id 
                ? 'border-l-4 border-l-teal-400 bg-white/8' 
                : ''
              }
            `}
          >
            <div className="space-y-1">
              <h3 className={`
                font-medium text-sm transition-colors
                ${activeSection === section.id 
                  ? 'text-white' 
                  : 'text-gray-400'
                }
              `}>
                {section.title}
              </h3>
              {section.description && (
                <p className="text-xs text-gray-500 line-clamp-2">
                  {section.description}
                </p>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SectionBlock;
