from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site, Page
from portfolio.models import (
    HomePage, ServiceItem, AboutFeature, AboutPage, ContactPage,
    CompanyValue, TeamMember, ContactMethod, ContactSubmission,
    ServicesPage, ServicePageItem, TeamPage, TeamPageMember, 
    BlogIndexPage, BlogPost, PortfolioIndexPage, ProjectPage
)


class Command(BaseCommand):
    help = 'Seed the database with initial Wagtail content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        if options['clean']:
            self.stdout.write('Cleaning existing data...')
            # Delete all pages except root
            Page.objects.filter(depth__gt=1).delete()
            ContactSubmission.objects.all().delete()
            self.stdout.write('Existing data cleaned.')
        
        # Get or create root page
        try:
            root_page = Page.objects.get(id=1)
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR('Root page not found. Please run migrations first.'))
            return

        # Ensure site exists
        site, created = Site.objects.get_or_create(
            hostname='localhost',
            defaults={
                'port': 8000,
                'site_name': 'Fintaa Software House',
                'root_page': root_page,
                'is_default_site': True
            }
        )
        if created:
            self.stdout.write('Created default site')

        # Delete existing homepage if it exists
        try:
            existing_home = HomePage.objects.filter(slug='home').first()
            if existing_home:
                existing_home.delete()
                self.stdout.write('Deleted existing homepage')
        except Exception as e:
            self.stdout.write(f'No existing homepage to delete: {e}')

        # Check if Welcome page exists and delete it
        try:
            welcome_page = Page.objects.filter(slug='home').first()
            if welcome_page and not isinstance(welcome_page, HomePage):
                welcome_page.delete()
                self.stdout.write('Deleted default welcome page')
        except Exception as e:
            self.stdout.write(f'Error deleting welcome page: {e}')

        # Create homepage
        self.stdout.write('Creating homepage...')
        home_page = HomePage(
            title="Fintaa Software House",
            slug="home",
            hero_title="Fintaa",
            hero_subtitle="TECH HOUSE",
            hero_typing_text="Transforming Ideas into Digital Reality...",
            hero_description="<p>Pakistan's Premier Software Development Company - Specializing in cutting-edge technology solutions, from web development to AI agents, we deliver excellence in every project.</p>",
            about_title="About Fintaa",
            about_description="<p>Registered in Pakistan as a sole proprietorship, Fintaa Software House is your trusted partner in digital transformation. We specialize in solving complex technical challenges with innovative solutions.</p>",
            about_additional_text="<p>Our expertise spans across multiple technology stacks and frameworks, ensuring we can handle any project from simple WordPress sites to complex AI-powered applications.</p>",
            technologies_count="50+",
            projects_count="100+",
            client_satisfaction="95%",
            years_experience="5+",
            contact_email="info@Fintaa.pk",
            contact_location="Pakistan",
            business_hours="24/7 Available"
        )
        
        # Use a safer method to add the page
        try:
            home_page = root_page.add_child(instance=home_page)
            revision = home_page.save_revision()
            revision.publish()
            self.stdout.write(f'Created homepage: {home_page.title}')
        except Exception as e:
            self.stdout.write(f'Error creating homepage: {e}')
            # Fallback: try to create a simpler page first
            try:
                # Create a simple page first to establish the tree
                temp_page = Page(title="temp", slug="temp")
                temp_page = root_page.add_child(instance=temp_page)
                temp_page.delete()
                
                # Now try to create the homepage again
                home_page = root_page.add_child(instance=home_page)
                revision = home_page.save_revision()
                revision.publish()
                self.stdout.write(f'Created homepage on second attempt: {home_page.title}')
            except Exception as e2:
                self.stdout.write(f'Failed to create homepage: {e2}')
                return
        
        # Update site to use our homepage
        site.root_page = home_page
        site.save()

        # Add services to homepage
        services_data = [
            {
                'title': 'Web Development',
                'description': 'Full-stack web solutions using modern frameworks like React, Node.js, Python Django, and Ruby on Rails.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>',
                'feature_1': 'Responsive Design',
                'feature_2': 'WordPress & Shopify',
                'feature_3': 'Custom Web Applications'
            },
            {
                'title': 'Mobile App Development',
                'description': 'Native and cross-platform mobile applications for iOS and Android with cutting-edge features.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a1 1 0 001-1V4a1 1 0 00-1-1H8a1 1 0 00-1 1v16a1 1 0 001 1z"></path></svg>',
                'feature_1': 'React Native',
                'feature_2': 'Flutter Development',
                'feature_3': 'iOS & Android Native'
            },
            {
                'title': 'AI & Automation',
                'description': 'Intelligent automation solutions, chatbots, and AI agents to streamline your business processes.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>',
                'feature_1': 'Custom AI Agents',
                'feature_2': 'Chatbot Development',
                'feature_3': 'Process Automation'
            },
            {
                'title': 'Cybersecurity',
                'description': 'Comprehensive security solutions to protect your digital assets and infrastructure.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>',
                'feature_1': 'Security Audits',
                'feature_2': 'Network Security',
                'feature_3': 'Penetration Testing'
            },
            {
                'title': 'Digital Marketing',
                'description': 'Strategic digital marketing solutions to boost your online presence and drive growth.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>',
                'feature_1': 'SEO Optimization',
                'feature_2': 'Social Media Marketing',
                'feature_3': 'Content Strategy'
            },
            {
                'title': 'Call Center & Support',
                'description': 'Professional call center services and customer support solutions for your business.',
                'icon_svg': '<svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>',
                'feature_1': '24/7 Support',
                'feature_2': 'Multi-language Support',
                'feature_3': 'CRM Integration'
            }
        ]

        for service_data in services_data:
            ServiceItem.objects.create(
                page=home_page,
                sort_order=len(home_page.services.all()),
                **service_data
            )

        # Add about features
        about_features = [
            "Registered Software House in Pakistan",
            "Expert Team of Developers & Engineers",
            "100+ Successful Projects Delivered",
            "24/7 Customer Support",
            "Agile Development Methodology",
            "Quality Assurance & Testing"
        ]

        for feature_text in about_features:
            AboutFeature.objects.create(
                page=home_page,
                sort_order=len(home_page.about_features.all()),
                feature_text=feature_text
            )

        self.stdout.write(self.style.SUCCESS('Homepage created successfully!'))

        # Create About Page
        self.stdout.write('Creating about page...')
        about_page = AboutPage(
            title="About Us",
            slug="about",
            hero_title="About Fintaa Software House",
            hero_subtitle="Your Trusted Technology Partner",
            hero_description="<p>Empowering businesses through innovative technology solutions since 2019. We are a registered software house in Pakistan dedicated to delivering excellence in every project.</p>",
            story_title="Our Story",
            story_content="<p>Founded in 2019, Fintaa Software House emerged from a passion for technology and a vision to transform businesses through innovative digital solutions. What started as a small team of dedicated developers has grown into Pakistan's premier software development company.</p><p>Our journey began with a simple mission: to bridge the gap between complex technology and business needs. Over the years, we've successfully delivered over 100 projects, helping businesses of all sizes achieve their digital transformation goals.</p>",
            mission_title="Our Mission",
            mission_content="<p>To empower businesses worldwide by delivering cutting-edge technology solutions that drive growth, efficiency, and innovation. We strive to be the trusted partner that transforms ideas into digital reality.</p>",
            vision_title="Our Vision",
            vision_content="<p>To become the leading software development company in Pakistan and expand globally, known for our technical excellence, innovative solutions, and commitment to client success.</p>"
        )
        
        home_page.add_child(instance=about_page)
        about_page.save_revision().publish()

        # Add company values
        values_data = [
            {
                'title': 'Innovation',
                'description': 'We embrace cutting-edge technologies and creative solutions to solve complex challenges.',
                'icon_name': 'lightbulb'
            },
            {
                'title': 'Quality',
                'description': 'We maintain the highest standards in code quality, testing, and project delivery.',
                'icon_name': 'verified'
            },
            {
                'title': 'Transparency',
                'description': 'We believe in open communication and keeping our clients informed throughout the project.',
                'icon_name': 'visibility'
            },
            {
                'title': 'Reliability',
                'description': 'Our clients can count on us to deliver projects on time and within budget.',
                'icon_name': 'schedule'
            },
            {
                'title': 'Partnership',
                'description': 'We work as an extension of your team, understanding your business goals and challenges.',
                'icon_name': 'handshake'
            },
            {
                'title': 'Growth',
                'description': 'We are committed to continuous learning and helping our clients scale their businesses.',
                'icon_name': 'trending_up'
            }
        ]

        for value_data in values_data:
            CompanyValue.objects.create(
                page=about_page,
                sort_order=len(about_page.values.all()),
                **value_data
            )

        # Add team members
        team_data = [
            {
                'name': 'Khalid Zaheer',
                'position': 'CEO & Lead Developer',
                'bio': 'Experienced full-stack developer with expertise in modern web technologies and AI solutions.',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face',
                'linkedin_url': 'https://linkedin.com/in/khalidzaheer',
                'github_url': 'https://github.com/khalidzaheer'
            },
            {
                'name': 'Sarah Ahmed',
                'position': 'UI/UX Designer',
                'bio': 'Creative designer focused on user-centered design and modern interface solutions.',
                'image_url': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=300&fit=crop&crop=face',
                'linkedin_url': 'https://linkedin.com/in/sarahahmed'
            },
            {
                'name': 'Muhammad Ali',
                'position': 'Mobile App Developer',
                'bio': 'Specialist in React Native and Flutter development with 5+ years of experience.',
                'image_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face',
                'github_url': 'https://github.com/muhammadali'
            }
        ]

        for member_data in team_data:
            TeamMember.objects.create(
                page=about_page,
                sort_order=len(about_page.team_members.all()),
                **member_data
            )

        self.stdout.write(self.style.SUCCESS('About page created successfully!'))

        # Create Contact Page
        self.stdout.write('Creating contact page...')
        contact_page = ContactPage(
            title="Contact Us",
            slug="contact",
            hero_title="Get In Touch",
            hero_description="<p>Ready to transform your ideas into reality? Let's discuss your next project and explore how we can help your business grow through innovative technology solutions.</p>",
            office_address="Lahore, Punjab\nPakistan",
            email_address="info@Fintaa.pk",
            phone_number="+92 300 1234567",
            business_hours="Monday - Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM\nSunday: Closed\n24/7 Emergency Support Available"
        )
        
        home_page.add_child(instance=contact_page)
        contact_page.save_revision().publish()

        # Add contact methods
        contact_methods_data = [
            {
                'title': 'WhatsApp',
                'description': '+92 300 1234567',
                'link': 'https://wa.me/923001234567',
                'icon_name': 'chat'
            },
            {
                'title': 'Skype',
                'description': 'Fintaa.software',
                'link': 'skype:Fintaa.software?chat',
                'icon_name': 'video_call'
            },
            {
                'title': 'LinkedIn',
                'description': 'Follow us on LinkedIn',
                'link': 'https://linkedin.com/company/Fintaa-software',
                'icon_name': 'business'
            }
        ]

        for method_data in contact_methods_data:
            ContactMethod.objects.create(
                page=contact_page,
                sort_order=len(contact_page.contact_methods.all()),
                **method_data
            )

        self.stdout.write(self.style.SUCCESS('Contact page created successfully!'))

        # Create sample contact submissions
        self.stdout.write('Creating sample contact submissions...')
        sample_contacts = [
            {
                'name': 'John Smith',
                'email': 'john.smith@example.com',
                'phone': '+1 555 0123',
                'company': 'Tech Innovations Inc.',
                'service': 'web_development',
                'budget': '15k_50k',
                'timeline': '3_months',
                'message': 'We need a modern e-commerce website with payment integration and inventory management.',
                'is_responded': False
            },
            {
                'name': 'Maria Garcia',
                'email': 'maria.garcia@startup.com',
                'phone': '+1 555 0456',
                'company': 'StartupXYZ',
                'service': 'mobile_app_development',
                'budget': '5k_15k',
                'timeline': '6_months',
                'message': 'Looking for a mobile app for our food delivery service. Need both iOS and Android versions.',
                'is_responded': True
            },
            {
                'name': 'Ahmed Hassan',
                'email': 'ahmed@techsolutions.ae',
                'company': 'Tech Solutions UAE',
                'service': 'ai_automation',
                'budget': '50k_plus',
                'timeline': 'flexible',
                'message': 'Interested in implementing AI chatbot and automation solutions for our customer service.',
                'is_responded': False
            }
        ]

        for contact_data in sample_contacts:
            ContactSubmission.objects.create(**contact_data)

        self.stdout.write(self.style.SUCCESS('Sample contact submissions created!'))

        # Create Services Page
        self.stdout.write('Creating services page...')
        services_page = ServicesPage(
            title="Our Services",
            slug="services",
            hero_title="Our Services",
            hero_description="<p>We offer comprehensive software development services to transform your ideas into reality. From web applications to AI solutions, we deliver excellence in every project.</p>"
        )
        home_page.add_child(instance=services_page)
        services_page.save_revision().publish()

        # Add services to Services page
        services_data = [
            {
                'title': 'Web Development',
                'description': '<p>Custom web applications built with modern frameworks and technologies. Responsive, fast, and user-friendly designs.</p>',
                'icon': 'fas fa-code',
                'features': '<ul><li>React, Vue.js, Django development</li><li>E-commerce solutions</li><li>CMS development</li><li>API integration</li></ul>'
            },
            {
                'title': 'Mobile App Development',
                'description': '<p>Native and cross-platform mobile applications for iOS and Android with seamless user experiences.</p>',
                'icon': 'fas fa-mobile-alt',
                'features': '<ul><li>Flutter & React Native</li><li>Native iOS & Android</li><li>App Store optimization</li><li>Push notifications</li></ul>'
            },
            {
                'title': 'AI & Machine Learning',
                'description': '<p>Cutting-edge AI solutions including chatbots, recommendation systems, and data analytics platforms.</p>',
                'icon': 'fas fa-brain',
                'features': '<ul><li>Natural Language Processing</li><li>Computer Vision</li><li>Predictive Analytics</li><li>Custom AI agents</li></ul>'
            },
            {
                'title': 'Cloud Solutions',
                'description': '<p>Scalable cloud infrastructure and deployment solutions for modern applications and data management.</p>',
                'icon': 'fas fa-cloud',
                'features': '<ul><li>AWS, Azure, GCP deployment</li><li>Docker & Kubernetes</li><li>CI/CD pipelines</li><li>Database management</li></ul>'
            },
            {
                'title': 'UI/UX Design',
                'description': '<p>Beautiful, intuitive designs that enhance user experience and drive engagement across all platforms.</p>',
                'icon': 'fas fa-paint-brush',
                'features': '<ul><li>User research & testing</li><li>Wireframing & prototyping</li><li>Brand identity design</li><li>Responsive design</li></ul>'
            },
            {
                'title': 'Digital Consulting',
                'description': '<p>Strategic technology consulting to help businesses leverage digital transformation for growth.</p>',
                'icon': 'fas fa-lightbulb',
                'features': '<ul><li>Technology audit</li><li>Digital strategy planning</li><li>Process optimization</li><li>Innovation roadmaps</li></ul>'
            }
        ]

        for service_data in services_data:
            ServicePageItem.objects.create(
                page=services_page,
                sort_order=len(services_page.service_items.all()),
                **service_data
            )

        self.stdout.write(self.style.SUCCESS('Services page created successfully!'))

        # Create Team Page
        self.stdout.write('Creating team page...')
        team_page = TeamPage(
            title="Our Team",
            slug="team",
            hero_title="Meet Our Team",
            hero_description="<p>Our talented team of developers, designers, and strategists work together to create exceptional software solutions that drive business success.</p>"
        )
        home_page.add_child(instance=team_page)
        team_page.save_revision().publish()

        # Add team members
        team_members_data = [
            {
                'name': 'Khalid Zaheer',
                'position': 'Founder & Lead Developer',
                'bio': '<p>Full-stack developer with expertise in modern web technologies and AI development. Passionate about creating innovative solutions that solve real-world problems.</p>',
                'email': 'wasay@Fintaa.pk',
                'linkedin': 'https://linkedin.com/in/khalidzaheer',
                'github': 'https://github.com/khalidzaheer',
                'skills': 'Python, Django, React, AI/ML, Cloud Computing'
            },
            {
                'name': 'Sarah Johnson',
                'position': 'Senior Frontend Developer',
                'bio': '<p>Creative frontend developer specializing in React and Vue.js. Expert in creating beautiful, responsive user interfaces with perfect attention to detail.</p>',
                'email': 'sarah@Fintaa.pk',
                'linkedin': 'https://linkedin.com/in/sarahjohnson',
                'github': 'https://github.com/sarahjohnson',
                'skills': 'React, Vue.js, TypeScript, CSS, UI/UX Design'
            },
            {
                'name': 'Ahmed Hassan',
                'position': 'Backend Developer',
                'bio': '<p>Experienced backend developer with strong expertise in Python, Node.js, and database design. Focuses on scalable architecture and API development.</p>',
                'email': 'ahmed@Fintaa.pk',
                'linkedin': 'https://linkedin.com/in/ahmedhassan',
                'github': 'https://github.com/ahmedhassan',
                'skills': 'Python, Node.js, PostgreSQL, MongoDB, Docker'
            },
            {
                'name': 'Emily Chen',
                'position': 'UI/UX Designer',
                'bio': '<p>Creative designer passionate about user-centered design. Specializes in creating intuitive interfaces that enhance user experience and drive engagement.</p>',
                'email': 'emily@Fintaa.pk',
                'linkedin': 'https://linkedin.com/in/emilychen',
                'skills': 'Figma, Adobe XD, User Research, Prototyping, Brand Design'
            }
        ]

        for member_data in team_members_data:
            TeamPageMember.objects.create(
                page=team_page,
                sort_order=len(team_page.team_members.all()),
                **member_data
            )

        self.stdout.write(self.style.SUCCESS('Team page created successfully!'))

        # Create Blog Index Page
        self.stdout.write('Creating blog page...')
        blog_page = BlogIndexPage(
            title="Blog",
            slug="blog",
            hero_title="Latest Insights",
            hero_description="<p>Stay updated with the latest in technology, development insights, and industry trends. Our team shares knowledge and experiences from the world of software development.</p>"
        )
        home_page.add_child(instance=blog_page)
        blog_page.save_revision().publish()

        # Create a sample blog post
        sample_post = BlogPost(
            title="The Future of Web Development in 2025",
            slug="future-web-development-2025",
            excerpt="Explore the latest trends and technologies shaping the future of web development, from AI integration to new frameworks.",
            author="Fintaa Team",
            publish_date=timezone.now().date(),
            content='[{"type": "heading", "value": "Introduction"}, {"type": "paragraph", "value": "<p>The web development landscape continues to evolve rapidly, with new technologies and frameworks emerging every year. In this article, we explore the key trends that will shape web development in 2025.</p>"}, {"type": "heading", "value": "Key Trends"}, {"type": "list", "value": ["AI-powered development tools", "WebAssembly adoption", "Progressive Web Apps", "Serverless architecture", "Low-code/no-code platforms"]}]',
            tags="web development, trends, 2025, technology"
        )
        blog_page.add_child(instance=sample_post)
        sample_post.save_revision().publish()

        self.stdout.write(self.style.SUCCESS('Blog page created successfully!'))

        # Create Portfolio Index Page
        self.stdout.write('Creating portfolio page...')
        portfolio_page = PortfolioIndexPage(
            title="Portfolio",
            slug="portfolio",
            hero_title="Our Portfolio",
            hero_description="<p>Explore our successful projects and see how we've helped businesses transform their digital presence with innovative technology solutions.</p>"
        )
        home_page.add_child(instance=portfolio_page)
        portfolio_page.save_revision().publish()

        # Create sample projects
        project_1 = ProjectPage(
            title="E-Commerce Platform",
            slug="ecommerce-platform",
            project_title="Modern E-Commerce Platform",
            project_subtitle="Full-Stack Development",
            client_name="TechRetail Co.",
            project_overview="<p>A comprehensive e-commerce solution built with React, Node.js, and PostgreSQL. Features include real-time inventory management, secure payment processing, and advanced analytics dashboard.</p>",
            project_challenge="<p>The client needed a scalable e-commerce platform that could handle high traffic volumes while providing excellent user experience across all devices.</p>",
            project_solution="<p>We implemented a modern microservices architecture with React frontend, Node.js backend, and PostgreSQL database. Added real-time features using WebSockets and integrated multiple payment gateways.</p>",
            project_results="<p>Achieved 40% increase in conversion rates, 60% improvement in page load times, and successfully handled Black Friday traffic with zero downtime.</p>",
            project_duration="4 months",
            project_team_size="5 developers",
            completion_date=timezone.now().date(),
            featured_image_url="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop"
        )
        portfolio_page.add_child(instance=project_1)
        project_1.save_revision().publish()

        project_2 = ProjectPage(
            title="AI Chatbot System",
            slug="ai-chatbot-system",
            project_title="Intelligent Customer Support Bot",
            project_subtitle="AI & Machine Learning",
            client_name="ServicePro Ltd.",
            project_overview="<p>An advanced AI-powered chatbot system using natural language processing to provide 24/7 customer support with high accuracy and customer satisfaction.</p>",
            project_challenge="<p>The client was struggling with high customer support costs and long response times, especially during peak hours and weekends.</p>",
            project_solution="<p>Developed an intelligent chatbot using OpenAI GPT models, integrated with the client's CRM system, and implemented sentiment analysis for escalation to human agents when needed.</p>",
            project_results="<p>Reduced customer support costs by 70%, improved response time to under 30 seconds, and achieved 85% customer satisfaction rate.</p>",
            project_duration="3 months",
            project_team_size="3 developers",
            completion_date=timezone.now().date(),
            featured_image_url="https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=600&h=400&fit=crop"
        )
        portfolio_page.add_child(instance=project_2)
        project_2.save_revision().publish()

        project_3 = ProjectPage(
            title="Mobile Banking App",
            slug="mobile-banking-app",
            project_title="Secure Mobile Banking Application",
            project_subtitle="Mobile Development",
            client_name="SecureBank",
            project_overview="<p>A comprehensive mobile banking application built with React Native, featuring biometric authentication, real-time transactions, and advanced security measures.</p>",
            project_challenge="<p>Creating a secure, user-friendly mobile banking experience that meets strict financial regulations while providing modern features customers expect.</p>",
            project_solution="<p>Implemented end-to-end encryption, biometric authentication, real-time fraud detection, and intuitive UI/UX design following banking compliance standards.</p>",
            project_results="<p>Increased mobile engagement by 300%, reduced transaction processing time by 50%, and achieved 99.9% uptime with zero security incidents.</p>",
            project_duration="6 months",
            project_team_size="7 developers",
            completion_date=timezone.now().date(),
            featured_image_url="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=400&fit=crop"
        )
        portfolio_page.add_child(instance=project_3)
        project_3.save_revision().publish()

        self.stdout.write(self.style.SUCCESS('Portfolio page created successfully!'))

        # Update site configuration
        site.root_page = home_page
        site.hostname = 'localhost'
        site.port = 8000
        site.is_default_site = True
        site.save()

        self.stdout.write(self.style.SUCCESS('Site configuration updated!'))
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Database seeding completed successfully!\n\n'
                'You can now:\n'
                '1. Visit the Wagtail CMS admin at: http://localhost:8000/cms/\n'
                '2. Visit the Unfold Django admin at: http://localhost:8000/django-admin/\n'
                '3. View your site at: http://localhost:8000/\n\n'
                'Default admin credentials:\n'
                'Username: admin\n'
                'Password: (the one you created)\n'
            )
        )
