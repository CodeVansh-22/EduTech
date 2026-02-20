const courses = [
    {
        title: "Full-Stack Web Development",
        description: "Master HTML, CSS, JavaScript, Node.js, and build dynamic web applications from scratch.",
        price: 4999,
        image: "assets/images/Course Card1.jpg"
    },
    {
        title: "Python & Data Science",
        description: "Learn Python, Pandas, Machine Learning Models, and complete real industry projects.",
        price: 6999,
        image: "assets/images/Course Card2.jpg"
    },
    {
        title: "Linux System Administration",
        description: "Master TCP/IP networking, firewalls, and server management for enterprise environments.",
        price: 3999,
        image: "assets/images/Course Card3.jpg"
    },
    {
        title: "Android App Development",
        description: "Build robust Android applications using Java & Kotlin with modern architecture.",
        price: 5999,
        image: "assets/images/Course Card4.jpg"
    },
    {
        title: "Digital Marketing Expert",
        description: "Master SEO, Social Media Marketing, and high-converting Ads Strategy.",
        price: 4499,
        image: "assets/images/Course Card5.jpg"
    },
    {
        title: "Generative AI & ChatGPT",
        description: "Learn Prompt Engineering, AI Automation, and how to build intelligent systems.",
        price: 7999,
        image: "assets/images/Course Card6.jpg"
    }
];

const container = document.getElementById("coursesContainer");

if (container) {
    courses.forEach(course => {
        // Notice the addition of the "glass" class here
        const card = `
            <div class="course-card glass">
                <img src="${course.image}" alt="${course.title}">
                <div class="course-content">
                    <h3>${course.title}</h3>
                    <p>${course.description}</p>
                    <div class="price">₹${course.price}</div>
                    <button class="btn-primary">Enroll Now</button>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}