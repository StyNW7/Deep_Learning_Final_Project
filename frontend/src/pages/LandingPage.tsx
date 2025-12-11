import { useState, useEffect } from 'react';
import { Wind, Map, TrendingDown, Bell, ArrowRight, Menu, X } from 'lucide-react';
import { useNavigate } from 'react-router';

// Navigation Component
const Navigation = () => {

  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/95 backdrop-blur-sm shadow-sm' : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <Wind className="w-6 h-6" />
            <span className="text-xl font-bold">AeroSeoul</span>
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#home" className="text-sm hover:text-gray-600 transition-colors">Home</a>
            <a href="#about" className="text-sm hover:text-gray-600 transition-colors">About</a>
            <a href="#features" className="text-sm hover:text-gray-600 transition-colors">Features</a>
            <button className="px-4 py-2 bg-black text-white text-sm rounded-full hover:bg-gray-800 transition-all duration-300 hover:scale-105">
              Get Started
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 space-y-3 animate-fadeIn">
            <a href="#home" className="block text-sm hover:text-gray-600 transition-colors">Home</a>
            <a href="#about" className="block text-sm hover:text-gray-600 transition-colors">About</a>
            <a href="#features" className="block text-sm hover:text-gray-600 transition-colors">Features</a>
            <button className="w-full px-4 py-2 bg-black text-white text-sm rounded-full hover:bg-gray-800 transition-colors">
              Get Started
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

// Footer Component
const Footer = () => {
  return (
    <footer className="bg-black text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Wind className="w-6 h-6" />
              <span className="text-xl font-bold">AeroSeoul</span>
            </div>
            <p className="text-gray-400 text-sm max-w-md">
              Real-time air quality monitoring and forecasting for Seoul. 
              Stay informed, breathe better.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#home" className="hover:text-white transition-colors">Home</a></li>
              <li><a href="#about" className="hover:text-white transition-colors">About</a></li>
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#map" className="hover:text-white transition-colors">Map</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>Seoul, South Korea</li>
              <li>info@aeroseoul.com</li>
              <li>+82 2 1234 5678</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400">
          <p>© 2025 AeroSeoul. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

// Main Landing Page Component
const LandingPage = () => {

  const navigate = useNavigate();
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null);

  const features = [
    {
      icon: <Wind className="w-8 h-8" />,
      title: "Real-Time Monitoring",
      description: "Live air quality data updated every hour from multiple monitoring stations across Seoul."
    },
    {
      icon: <TrendingDown className="w-8 h-8" />,
      title: "7-Day Forecast",
      description: "Advanced AI-powered predictions to help you plan your week with confidence."
    },
    {
      icon: <Bell className="w-8 h-8" />,
      title: "Smart Alerts",
      description: "Receive personalized notifications when air quality changes in your area."
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Navigation />
      
      {/* Hero Section */}
      <section id="home" className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center animate-fadeInUp">
            <div className="inline-block mb-4 px-4 py-2 bg-gray-100 rounded-full text-sm font-medium animate-slideDown">
              Real-time Air Quality Insights
            </div>
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight animate-fadeInUp" style={{animationDelay: '0.1s'}}>
              Breathe Easy in
              <br />
              <span className="relative inline-block">
                Seoul
                <svg className="absolute -bottom-2 left-0 w-full animate-drawLine" height="12" viewBox="0 0 200 12">
                  <path d="M0 6 Q50 0, 100 6 T200 6" stroke="black" strokeWidth="2" fill="none" />
                </svg>
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto animate-fadeInUp" style={{animationDelay: '0.2s'}}>
              Stay ahead of air pollution with accurate forecasts and real-time monitoring. 
              Your health, our priority.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fadeInUp" style={{animationDelay: '0.3s'}}>
              <button className="px-8 py-4 bg-black text-white rounded-full hover:bg-gray-800 transition-all duration-300 hover:scale-105 hover:shadow-xl flex items-center justify-center space-x-2 group" onClick={() => navigate('/map')}>
                <span>Explore Now</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="px-8 py-4 border-2 border-black text-black rounded-full hover:bg-black hover:text-white transition-all duration-300 hover:scale-105">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="animate-fadeInLeft">
              <h2 className="text-4xl font-bold mb-6">Why AeroSeoul?</h2>
              <p className="text-gray-600 mb-4 leading-relaxed">
                Seoul faces unique air quality challenges due to its dense urban environment and geographical location. 
                AeroSeoul combines cutting-edge technology with local expertise to provide you with the most accurate 
                air quality information.
              </p>
              <p className="text-gray-600 leading-relaxed">
                Our platform uses advanced machine learning algorithms trained on years of historical data to predict 
                air quality patterns, helping you make informed decisions about your outdoor activities.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4 animate-fadeInRight">
              <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <div className="text-3xl font-bold mb-2">98%</div>
                <div className="text-sm text-gray-600">Accuracy Rate</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 mt-8">
                <div className="text-3xl font-bold mb-2">50+</div>
                <div className="text-sm text-gray-600">Monitoring Stations</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <div className="text-3xl font-bold mb-2">24/7</div>
                <div className="text-sm text-gray-600">Live Updates</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 mt-8">
                <div className="text-3xl font-bold mb-2">7-Day</div>
                <div className="text-sm text-gray-600">Forecasting</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Map Section */}
      <section id="map" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4 animate-fadeInUp">Explore Seoul's Air Quality</h2>
          <p className="text-gray-600 mb-12 animate-fadeInUp" style={{animationDelay: '0.1s'}}>
            Interactive map with real-time data from all districts
          </p>
          <div 
            className="relative group cursor-pointer overflow-hidden rounded-3xl border-4 border-black hover:border-gray-700 transition-all duration-500 animate-fadeInUp"
            style={{animationDelay: '0.2s'}}
            onClick={() => navigate('/map')}
          >
            <div className="aspect-video bg-linear-to-br from-gray-100 to-gray-200 flex items-center justify-center relative overflow-hidden">
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-all duration-500" />
              <div className="text-center z-10 transform group-hover:scale-105 transition-transform duration-500">
                <Map className="w-24 h-24 mx-auto mb-4 opacity-30 group-hover:opacity-50 transition-opacity" />
                <p className="text-2xl font-semibold text-gray-700 group-hover:text-black transition-colors">
                  Click to View Interactive Map
                </p>
                <div className="mt-4 inline-flex items-center space-x-2 text-gray-600 group-hover:text-black transition-colors">
                  <span>Explore Districts</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform" />
                </div>
              </div>
              <div className="absolute inset-0 border-2 border-black/0 group-hover:border-black/20 rounded-3xl transition-all duration-500 scale-95 group-hover:scale-100" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 animate-fadeInUp">Powerful Features</h2>
            <p className="text-gray-600 animate-fadeInUp" style={{animationDelay: '0.1s'}}>
              Everything you need to stay informed about air quality
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white p-8 rounded-2xl hover:shadow-2xl transition-all duration-500 cursor-pointer group animate-fadeInUp border-2 border-transparent hover:border-black"
                style={{animationDelay: `${0.1 * index}s`}}
                onMouseEnter={() => setHoveredFeature(index)}
                onMouseLeave={() => setHoveredFeature(null)}
              >
                <div className={`mb-6 transform transition-all duration-500 ${
                  hoveredFeature === index ? 'scale-110 rotate-3' : 'scale-100'
                }`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3 group-hover:translate-x-2 transition-transform duration-300">
                  {feature.title}
                </h3>
                <p className="text-gray-600 group-hover:text-gray-900 transition-colors">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-black text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 animate-fadeInUp">
            Ready to Breathe Easier?
          </h2>
          <p className="text-xl text-gray-300 mb-10 animate-fadeInUp" style={{animationDelay: '0.1s'}}>
            Join thousands of Seoul residents who trust AeroSeoul for their daily air quality updates.
          </p>
          <button className="px-10 py-4 bg-white text-black rounded-full hover:bg-gray-100 transition-all duration-300 hover:scale-105 hover:shadow-2xl text-lg font-semibold animate-fadeInUp flex items-center space-x-2 mx-auto group" style={{animationDelay: '0.2s'}} onClick={() => navigate('/map')}>
            <span>Start Monitoring Now</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </section>

      <Footer />

      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInLeft {
          from {
            opacity: 0;
            transform: translateX(-30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes fadeInRight {
          from {
            opacity: 0;
            transform: translateX(30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes drawLine {
          from {
            stroke-dasharray: 200;
            stroke-dashoffset: 200;
          }
          to {
            stroke-dasharray: 200;
            stroke-dashoffset: 0;
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease-out forwards;
        }

        .animate-fadeInLeft {
          animation: fadeInLeft 0.8s ease-out forwards;
        }

        .animate-fadeInRight {
          animation: fadeInRight 0.8s ease-out forwards;
        }

        .animate-slideDown {
          animation: slideDown 0.6s ease-out forwards;
        }

        .animate-drawLine {
          animation: drawLine 1.5s ease-out forwards;
          animation-delay: 0.5s;
          stroke-dasharray: 200;
          stroke-dashoffset: 200;
        }

        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default LandingPage;