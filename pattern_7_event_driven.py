#!/usr/bin/env python3
"""
PATTERN 7: EVENT-BASED / OBSERVER PATTERN
==========================================
AI subscribes to events and reacts to certificate generation lifecycle
Perfect for complex workflows and audit logging
"""

from typing import Callable, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput


class CertificateEventType(Enum):
    """Certificate generation events"""
    VALIDATION_START = "validation_start"
    VALIDATION_COMPLETE = "validation_complete"
    VALIDATION_FAILED = "validation_failed"
    GENERATION_START = "generation_start"
    GENERATION_COMPLETE = "generation_complete"
    GENERATION_FAILED = "generation_failed"


@dataclass
class CertificateEvent:
    """Event object passed to handlers"""
    event_type: CertificateEventType
    timestamp: str
    cn: str
    data: Dict[str, Any]
    error: str = None


class CertificateEventBus:
    """
    Publish-subscribe event bus for certificate operations
    AI can register event handlers and respond to lifecycle events
    """

    def __init__(self):
        self._handlers: Dict[CertificateEventType, List[Callable]] = {}

    def subscribe(self, event_type: CertificateEventType, handler: Callable):
        """
        Subscribe to an event type
        
        Args:
            event_type: CertificateEventType to listen for
            handler: Callable that accepts CertificateEvent
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: CertificateEvent):
        """Publish an event to all subscribers"""
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")


class EventDrivenCertificateGenerator:
    """
    Certificate generator with event notifications
    AI doesn't need to know internal details, just listens to events
    """

    def __init__(self, event_bus: CertificateEventBus = None):
        self.generator = CertificateGenerator()
        self.event_bus = event_bus or CertificateEventBus()

    def generate(self, params: CertificateParams) -> CertificateOutput:
        """Generate certificate with event notifications"""
        from datetime import datetime

        # Event: Generation started
        self.event_bus.publish(CertificateEvent(
            event_type=CertificateEventType.GENERATION_START,
            timestamp=datetime.now().isoformat(),
            cn=params.cn,
            data={"key_type": params.key_type, "strength": params.key_strength}
        ))

        try:
            # Validate parameters
            self.event_bus.publish(CertificateEvent(
                event_type=CertificateEventType.VALIDATION_START,
                timestamp=datetime.now().isoformat(),
                cn=params.cn,
                data={}
            ))

            # If validation would fail, it would throw here
            # Validation passed
            self.event_bus.publish(CertificateEvent(
                event_type=CertificateEventType.VALIDATION_COMPLETE,
                timestamp=datetime.now().isoformat(),
                cn=params.cn,
                data={"valid": True}
            ))

            # Do actual generation
            result = self.generator.generate(params)

            if result.success:
                # Event: Generation complete
                self.event_bus.publish(CertificateEvent(
                    event_type=CertificateEventType.GENERATION_COMPLETE,
                    timestamp=datetime.now().isoformat(),
                    cn=params.cn,
                    data={
                        "cert_path": result.cert_path,
                        "key_path": result.key_path
                    }
                ))
            else:
                # Event: Generation failed
                self.event_bus.publish(CertificateEvent(
                    event_type=CertificateEventType.GENERATION_FAILED,
                    timestamp=datetime.now().isoformat(),
                    cn=params.cn,
                    data={},
                    error=result.error
                ))

            return result

        except Exception as e:
            self.event_bus.publish(CertificateEvent(
                event_type=CertificateEventType.GENERATION_FAILED,
                timestamp=datetime.now().isoformat(),
                cn=params.cn,
                data={},
                error=str(e)
            ))
            return CertificateOutput(
                success=False,
                message="Generation failed",
                error=str(e)
            )


# Example event handlers
def logging_handler(event: CertificateEvent):
    """Handler that logs events"""
    print(f"[{event.event_type.value}] {event.cn}: {event.data}")


def audit_handler(event: CertificateEvent):
    """Handler that audits certificate operations"""
    if event.event_type == CertificateEventType.GENERATION_COMPLETE:
        print(f"AUDIT: Certificate created for {event.cn}")
        print(f"  Certificate: {event.data.get('cert_path')}")
        print(f"  Key: {event.data.get('key_path')}")


def error_handler(event: CertificateEvent):
    """Handler that tracks errors"""
    if event.event_type == CertificateEventType.GENERATION_FAILED:
        print(f"ERROR: Failed to generate certificate for {event.cn}")
        print(f"  Reason: {event.error}")


def notification_handler(event: CertificateEvent):
    """Handler that could send notifications (email, Slack, etc)"""
    if event.event_type == CertificateEventType.GENERATION_COMPLETE:
        # AI could implement: send_slack_message(f"Certificate ready for {event.cn}")
        pass


# AI usage pattern
def ai_pattern_7_event_driven():
    """
    Example: AI sets up event handlers and uses generator
    No knowledge of internal generator implementation
    """
    
    # Create event bus and generator
    event_bus = CertificateEventBus()
    generator = EventDrivenCertificateGenerator(event_bus)
    
    # AI subscribes to events
    event_bus.subscribe(CertificateEventType.GENERATION_START, logging_handler)
    event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, audit_handler)
    event_bus.subscribe(CertificateEventType.GENERATION_FAILED, error_handler)
    
    # AI can add specialized handlers
    event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, notification_handler)
    
    # AI uses generator - all handlers fire automatically
    params = CertificateParams(
        cn="event-driven.example.com",
        key_type="rsa",
        key_strength=2048
    )
    
    result = generator.generate(params)
    return result


if __name__ == "__main__":
    result = ai_pattern_7_event_driven()
    print(f"\nPattern 7 - Event-Based: {result.message}")
