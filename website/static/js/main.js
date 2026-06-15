/* -------------------------------------------------------------
   Patliputra Institute of Technology & Management (PITM) - Scripts
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Header Scroll Effect
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // 2. Mobile Nav Drawer Toggle
    const mobileToggle = document.querySelector('.mobile-nav-toggle');
    const closeDrawer = document.querySelector('.mobile-nav-close');
    const drawer = document.querySelector('.mobile-nav-drawer');
    const backdrop = document.querySelector('.backdrop');

    if (mobileToggle && drawer && backdrop) {
        const toggleDrawer = (open) => {
            if (open) {
                drawer.classList.add('open');
                backdrop.classList.add('open');
                document.body.style.overflow = 'hidden';
            } else {
                drawer.classList.remove('open');
                backdrop.classList.remove('open');
                document.body.style.overflow = '';
            }
        };

        mobileToggle.addEventListener('click', () => toggleDrawer(true));
        if (closeDrawer) closeDrawer.addEventListener('click', () => toggleDrawer(false));
        backdrop.addEventListener('click', () => toggleDrawer(false));
    }

    // 3. Hero Carousel Slider
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.slider-btn-prev');
    const nextBtn = document.querySelector('.slider-btn-next');
    
    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval;

        const showSlide = (n) => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (n + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
        };

        const nextSlide = () => showSlide(currentSlide + 1);
        const prevSlide = () => showSlide(currentSlide - 1);

        const startInterval = () => {
            slideInterval = setInterval(nextSlide, 5000); // Auto slide every 5 seconds
        };

        const stopInterval = () => {
            clearInterval(slideInterval);
        };

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                stopInterval();
                nextSlide();
                startInterval();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                stopInterval();
                prevSlide();
                startInterval();
            });
        }

        // Start slide show
        startInterval();
    }

    // 4. Gallery Filtering & Lightbox Modal
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxClose = document.getElementById('lightbox-close');

    if (galleryItems.length > 0) {
        // Dynamic Filter
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons and add to clicked
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filterValue = btn.getAttribute('data-filter');

                galleryItems.forEach(item => {
                    const category = item.getAttribute('data-category');
                    if (filterValue === 'all' || filterValue === category) {
                        item.style.display = 'block';
                        // Trigger fade in animation
                        item.style.opacity = '0';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transition = 'opacity 0.4s ease';
                        }, 50);
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });

        // Lightbox Popup
        galleryItems.forEach(item => {
            item.addEventListener('click', () => {
                const img = item.querySelector('.gallery-item-img');
                const title = item.querySelector('.gallery-overlay h4').innerText;
                
                if (lightbox && lightboxImg && lightboxCaption && img) {
                    lightboxImg.src = img.src;
                    lightboxCaption.innerText = title;
                    lightbox.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        if (lightboxClose && lightbox) {
            const closeLightbox = () => {
                lightbox.classList.remove('open');
                document.body.style.overflow = '';
            };

            lightboxClose.addEventListener('click', closeLightbox);
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
                    closeLightbox();
                }
            });
            // Esc key close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && lightbox.classList.contains('open')) {
                    closeLightbox();
                }
            });
        }
    }

    // 5. Contact Form Submission (AJAX submission with feedback)
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        const formAlert = document.getElementById('form-alert');
        const submitBtn = contactForm.querySelector('button[type="submit"]');

        const showAlert = (type, message) => {
            if (!formAlert) return;
            formAlert.innerHTML = `
                <div class="alert alert-${type === 'success' ? 'success' : 'danger'}">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                    <span>${message}</span>
                </div>
            `;
            formAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        };

        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Inputs
            const name = contactForm.name.value.trim();
            const email = contactForm.email.value.trim();
            const phone = contactForm.phone.value.trim();
            const subject = contactForm.subject.value.trim();
            const message = contactForm.message.value.trim();

            // Client-side Validations
            if (!name || !email || !phone || !subject || !message) {
                showAlert('error', 'Please fill in all the fields.');
                return;
            }

            // Email RegEx
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showAlert('error', 'Please enter a valid email address.');
                return;
            }

            // Phone RegEx (10 digits Indian style / general numbers)
            const phoneRegex = /^[0-9+\s-]{10,15}$/;
            if (!phoneRegex.test(phone)) {
                showAlert('error', 'Please enter a valid phone number (10-15 digits).');
                return;
            }

            // Disable submit button & show loading state
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending Message...';
            
            // Get CSRF Token
            const csrfToken = contactForm.querySelector('[name=csrfmiddlewaretoken]').value;

            // Submit request via fetch API
            fetch(contactForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    phone: phone,
                    subject: subject,
                    message: message
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                showAlert('success', data.message);
                contactForm.reset(); // Reset form fields
            })
            .catch(error => {
                console.error('Submission Error:', error);
                showAlert('error', error.message || 'An error occurred. Please try again later.');
            })
            .finally(() => {
                // Restore button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            });
        });
    }

    // 6. Leaflet Map Setup (Optional, triggers if map container exists)
    const mapElement = document.getElementById('map');
    if (mapElement && typeof L !== 'undefined') {
        // Patna coordinates: 25.6101° N, 85.1228° E (Bailey Road near High Court/Museum area)
        const patnaCoords = [25.6100, 85.1220]; 
        
        const map = L.map('map', {
            center: patnaCoords,
            zoom: 15,
            scrollWheelZoom: false // Disable scroll zoom for user friendliness
        });

        // Add OSM Tile Layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Custom Styled Pin icon
        const customIcon = L.divIcon({
            html: '<div style="background-color:#1e3a8a; border:3px solid #eab308; width:20px; height:20px; border-radius:50%; box-shadow:0 0 10px rgba(0,0,0,0.5);"></div>',
            className: 'custom-map-marker',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        // Add Marker
        L.marker(patnaCoords, { icon: customIcon })
            .addTo(map)
            .bindPopup(`
                <div style="font-family:'Outfit',sans-serif; text-align:center; padding:5px;">
                    <h4 style="margin:0 0 4px 0; color:#1e3a8a; font-weight:700;">PITM Campus</h4>
                    <p style="margin:0; font-size:12px; color:#64748b;">Bailey Road, Patna, Bihar</p>
                </div>
            `)
            .openPopup();
    }
});
