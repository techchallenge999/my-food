import logging

class DomainException(Exception):
    """Base class for domain-specific exceptions."""
    pass

class OrderNotFoundException(DomainException):
    """Exception raised when an order is not found."""
    pass

class InvalidPaymentException(DomainException):
    """Exception raised when a payment is invalid."""
    pass

class ErrorHandler:
    """Centralized error handling component."""

    def __init__(self):
        self.logger = logging.getLogger("ErrorHandler")

    def handle_error(self, error):
        """Handle the given error."""
        if isinstance(error, OrderNotFoundException):
            # Handle order not found error
            self.logger.error("Order not found: %s", str(error))
            # Log the error, notify relevant parties, etc.

        elif isinstance(error, InvalidPaymentException):
            # Handle invalid payment error
            self.logger.error("Invalid payment: %s", str(error))
            # Log the error, notify relevant parties, etc.

        else:
            # Handle generic error
            self.logger.error("An error occurred: %s", str(error))
            # Log the error, handle it as appropriate

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Example usage
error_handler = ErrorHandler()
try:
    # Retrieve order details
    # ...
    if order_not_found:
        raise OrderNotFoundException("Order not found.")

    # Process payment
    # ...
    if payment_invalid:
        raise InvalidPaymentException("Invalid payment details.")

except DomainException as e:
    # Pass the error to the centralized error handler
    error_handler.handle_error(e)
