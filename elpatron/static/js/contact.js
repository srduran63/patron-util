document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        
        try {
            const response = await fetch('/send-contact', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                alert('Mensaje enviado correctamente. Te contactaremos pronto.');
                this.reset();
            } else {
                throw new Error('Error al enviar el mensaje');
            }
        } catch (error) {
            alert('Error al enviar el mensaje. Por favor, intenta nuevamente.');
        } finally {
            submitButton.disabled = false;
        }
    });
});