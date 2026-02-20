document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. LOAD ALL COURSES (From MongoDB)
    // ==========================================
    const coursesContainer = document.getElementById("coursesContainer");
    
    if (coursesContainer) {
        coursesContainer.innerHTML = '<p style="color: #cbd5e1; text-align: center; width: 100%;">Loading courses from database...</p>';
        
        fetch('/api/courses')
            .then(response => response.json())
            .then(courses => {
                coursesContainer.innerHTML = ''; // Clear loading text
                
                courses.forEach(course => {
                    // encodeURI ensures that spaces in filenames (like "Course Card1.jpg") don't break the image!
                    const imgUrl = encodeURI(course.image);
                    
                    const card = `
                        <div class="course-card glass">
                            <img src="${imgUrl}" alt="${course.title}" onerror="this.src='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80'">
                            <div class="course-content">
                                <h3>${course.title}</h3>
                                <p>${course.description}</p>
                                <div class="price">₹${course.price}</div>
                                <button class="btn-primary" onclick="enrollCourse('${course.id}')">Enroll Now</button>
                            </div>
                        </div>
                    `;
                    coursesContainer.innerHTML += card;
                });
            })
            .catch(err => {
                console.error("Error fetching courses:", err);
                coursesContainer.innerHTML = '<p style="color: #ef4444; text-align: center; width: 100%;">Failed to connect to the database.</p>';
            });
    }
// ==========================================
    // 2. USER REGISTRATION LOGIC
    // ==========================================
    const registerForm = document.getElementById("registerForm");
    
    if (registerForm) {
        registerForm.addEventListener("submit", (e) => {
            e.preventDefault(); 
            
            // Get input values using their new IDs
            const fullName = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const role = document.getElementById('regRole').value; // Grab the selected role

            fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    full_name: fullName, 
                    email: email, 
                    password: password,
                    role: role // Send role to backend
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert(data.message);
                    window.location.href = '/login.html'; // Redirect to login
                }
            });
        });
    }

// ==========================================
    // 3. USER LOGIN LOGIC (SMART REDIRECT)
    // ==========================================
    const loginForm = document.getElementById("loginForm");
    
    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            
            // Using exact IDs to prevent errors
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    // Save user details to browser storage
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    // SMART REDIRECT: Check role and send to correct dashboard
                    if (data.user.role === 'admin') {
                        alert("Welcome Admin!");
                        window.location.href = '/admin-dashboard.html';
                    } else {
                        alert("Welcome Student!");
                        window.location.href = '/dashboard.html';
                    }
                }
            });
        });
    }
    // ==========================================
    // 4. LOAD STUDENT DASHBOARD (My Courses)
    // ==========================================
    if (window.location.pathname.includes("dashboard.html") && !window.location.pathname.includes("admin")) {
        // Check if user is actually logged in
        const userData = localStorage.getItem('user');
        if (!userData) {
            alert("You must be logged in to view your dashboard.");
            window.location.href = "/login.html";
            return;
        }

        const user = JSON.parse(userData);
        
        // Personalize the dashboard greeting
        const headerElement = document.querySelector('.page-header h2');
        if (headerElement) headerElement.innerText = `Welcome back, ${user.full_name}!`;

        const dashGrid = document.querySelector('.dashboard-grid');
        if (dashGrid) {
            dashGrid.innerHTML = '<p style="color: #cbd5e1; text-align: center; width: 100%;">Fetching your enrolled courses...</p>';
            
            fetch(`/api/my-courses/${user.id}`)
                .then(res => res.json())
                .then(courses => {
                    dashGrid.innerHTML = '';
                    
                    if (courses.length === 0) {
                        dashGrid.innerHTML = '<p style="color: #cbd5e1; text-align: center; width: 100%;">You haven\'t enrolled in any courses yet. <a href="/courses.html" style="color:#06b6d4;">Browse Courses</a></p>';
                    } else {
                        courses.forEach(course => {
                            const card = `
                                <div class="course-card glass">
                                    <div class="course-content">
                                        <h3 style="color:#06b6d4; margin-bottom: 5px;">${course.title}</h3>
                                        <p style="font-size: 12px; margin-bottom: 15px;">Enrolled on: ${course.enrolled_at}</p>
                                        <button class="btn-primary" style="background: #ec4899;">View Course Material</button>
                                    </div>
                                </div>
                            `;
                            dashGrid.innerHTML += card;
                        });
                    }
                });
        }
    }
});

// ==========================================
// 5. ENROLL IN COURSE LOGIC
// ==========================================
function enrollCourse(courseId) {
    const userData = localStorage.getItem('user');
    
    // Force user to login if they aren't
    if (!userData) {
        alert("Please login to enroll in courses.");
        window.location.href = '/login.html';
        return;
    }

    const user = JSON.parse(userData);

    fetch('/api/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, course_id: courseId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Will alert if already enrolled
        } else {
            alert(data.message);
            window.location.href = '/dashboard.html'; // Take them to their new course!
        }
    })
    .catch(err => console.error(err));
}
// ==========================================
// SHOW / HIDE PASSWORD TOGGLE
// ==========================================
function togglePassword(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈"; // Change to 'hide' icon
    } else {
        input.type = "password";
        icon.textContent = "👁️"; // Change back to 'eye' icon
    }
}