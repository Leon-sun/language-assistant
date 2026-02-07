"""
Weighted Interest Graph implementation for tracking user interests dynamically.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional
from django.utils import timezone


@dataclass
class Interest:
    """
    Represents a single interest with score, decay, and interaction tracking.
    """
    label: str
    score: float = 0.0
    last_updated: datetime = field(default_factory=timezone.now)
    interaction_count: int = 0
    decay_rate: float = 0.95  # Default decay rate per day
    
    def __post_init__(self):
        """Validate score is within bounds."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {self.score}")
        if not 0.0 < self.decay_rate <= 1.0:
            raise ValueError(f"Decay rate must be between 0.0 and 1.0, got {self.decay_rate}")
    
    def decay_score(self, current_time: Optional[datetime] = None) -> float:
        """
        Calculate decayed score based on time elapsed since last update.
        
        Formula: new_score = current_score * (decay_rate ^ days_passed)
        
        Args:
            current_time: Current datetime (defaults to timezone.now())
        
        Returns:
            float: Decayed score (0.0 to 1.0)
        """
        if current_time is None:
            current_time = timezone.now()
        
        # Calculate time difference
        time_diff = current_time - self.last_updated
        
        # Convert to days (as float for fractional days)
        days_passed = time_diff.total_seconds() / 86400.0  # 86400 seconds in a day
        
        # If no time has passed or negative time (shouldn't happen), return current score
        if days_passed <= 0:
            return self.score
        
        # Apply decay: new_score = current_score * (decay_rate ^ days_passed)
        decayed_score = self.score * (self.decay_rate ** days_passed)
        
        # Ensure score doesn't go below 0.0
        decayed_score = max(0.0, decayed_score)
        
        return decayed_score
    
    def to_dict(self) -> Dict:
        """Convert Interest to dictionary for serialization."""
        return {
            'label': self.label,
            'score': self.score,
            'last_updated': self.last_updated.isoformat(),
            'interaction_count': self.interaction_count,
            'decay_rate': self.decay_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Interest':
        """Create Interest from dictionary."""
        # Parse datetime string if needed
        if isinstance(data.get('last_updated'), str):
            from django.utils.dateparse import parse_datetime
            last_updated = parse_datetime(data['last_updated'])
            if last_updated:
                # Make timezone-aware if not already
                if timezone.is_naive(last_updated):
                    last_updated = timezone.make_aware(last_updated)
            else:
                last_updated = timezone.now()
        else:
            last_updated = data.get('last_updated', timezone.now())
        
        return cls(
            label=data['label'],
            score=data.get('score', 0.0),
            last_updated=last_updated,
            interaction_count=data.get('interaction_count', 0),
            decay_rate=data.get('decay_rate', 0.95)
        )
