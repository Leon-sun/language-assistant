import React from 'react';

const Card = ({ 
  children, 
  className = '', 
  variant = 'default',
  onClick,
  hover = false 
}) => {
  const baseClasses = 'glass rounded-xl p-6 transition-all duration-300';
  
  const variantClasses = {
    default: 'bg-white/5 border-white/10',
    strong: 'glass-strong bg-white/10 border-white/20',
    subtle: 'bg-white/3 border-white/5',
  };

  const hoverClasses = hover 
    ? 'hover:bg-white/10 hover:border-white/20 hover:shadow-glass-sm cursor-pointer' 
    : '';

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${hoverClasses} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

export default Card;
