import React from 'react';

const Navbar = ({ activeItem, onNavClick }) => {
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'getting-started', label: 'Getting Started' },
    { id: 'api', label: 'API Reference' },
    { id: 'examples', label: 'Examples' },
    { id: 'guides', label: 'Guides' },
  ];

  return (
    <nav className="glass sticky top-0 z-50 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">D</span>
            </div>
            <span className="text-white font-semibold text-lg">Dictionary</span>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center space-x-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavClick && onNavClick(item.id)}
                className={`
                  relative px-4 py-2 text-sm font-medium transition-all duration-200
                  ${activeItem === item.id
                    ? 'text-white accent-line'
                    : 'text-gray-400 hover:text-white'
                  }
                `}
              >
                {item.label}
                {activeItem === item.id && (
                  <span className="absolute bottom-0 left-0 h-0.5 w-full bg-gradient-to-r from-teal-400 to-teal-600"></span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
