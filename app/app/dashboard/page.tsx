import HomeNewsList from "@/components/general/HomeNewsList";
import { Event } from "../components/general/HomeNewsList"; // Import the custom Event type

async function getEventsData(): Promise<Event[]> {
  // This function can be used to fetch or generate event data
  return [
    // Active events
    {
      imageUrl: "/images/canada1.jpeg",
      title: "Avoid US Travel",
      category: "POLITICAL",
      location: "Canada",
      severity: "High",
      type: "active",
    },
    {
      imageUrl: "/images/asean.jpeg",
      title: "Trump tariffs, ASEAN should diversify",
      category: "POLITICAL",
      location: "Singapore",
      severity: "High",
      type: "active",
    },
    {
      imageUrl: "/images/canada1.jpeg",
      title: "Three ways this Canada-U.S. dispute will end",
      category: "POLITICAL",
      location: "Canada",
      severity: "Medium",
      type: "active",
    },
    {
      imageUrl: "/images/bengal.jpeg",
      title: "Mamata Banerjee fueling violence...: Kiren Rijiju slams Bengal CM's stand on Waqf Act, condemns violence in state",
      category: "POLITICAL",
      location: "India",
      severity: "High",
      type: "active",
    },
    // Potential events
    {
      imageUrl: "/images/election.jpeg",
      title: "Candidates’ election deposit remains at $13,500 for GE2025",
      category: "POLITICAL",
      location: "Singapore",
      severity: "Medium",
      type: "potential",
    },
    {
      imageUrl: "/images/heatwave/delhi-heatwave.jpg",
      title: "Reintroduce moral lessons to combat violence",
      category: "SOCIAL",
      location: "India",
      severity: "Medium",
      type: "potential",
    },
    {
      imageUrl: "/images/turtle.jpg",
      title: "Climate change is skewing sex ratios of Olive Ridley turtles hatching in Odisha",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Medium",
      type: "potential",
    },
    {
      imageUrl: "/images/canadabank.jpeg",
      title: "Bank of Canada holds rates at 2.75%, says trade war could cause a recession",
      category: "ECONOMIC",
      location: "Canada",
      severity: "Medium",
      type: "potential",
    }
  ];
}

export default async function Home() {
  const events: Event[] = await getEventsData();

  return (
    <div className="relative h-screen overflow-hidden">
      {/* Map Container with Horizontal Scroll */}
      <div className="absolute top-0 left-0 w-full h-full overflow-x-auto">
        <div className="h-full flex" style={{ width: "200%" }}>
          {/* First Map */}
          <div 
            className="h-full flex-1 bg-cover bg-no-repeat bg-center"
            style={{ backgroundImage: "url('/images/hmm.jpeg')" }}
          >
            {/* Red Dots for first map */}
            {/* <div className="absolute" style={{ top: '46%', left: '34.4%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">Alert!</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div> */}

            {/* <div className="absolute" style={{ top: '54.2%', left: '45.65%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">2 events of Medium Severity</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div> */}

            {/* <div className="absolute" style={{ top: '74.5%', left: '54%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">3 events of High Severity</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div> */}

            <div className="absolute" style={{ top: '16.5%', left: '18%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">
                3 events of High Severity
              </div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>
            <div 
            className="h-full flex-1 bg-cover bg-no-repeat bg-center"
            style={{ backgroundImage: "url('/images/hmm.jpeg')" }}
          >
            {/* Red Dots for second map - same dots, adjusted positions */}
            <div className="absolute" style={{ top: '58.9%', left: '176.1%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">2 events of High Severity</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>

              {/* Malaysia */}
            <div className="absolute" style={{ top: '56.6%', left: '179.9%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">Alert!</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>

              {/* #australia pg 2 */}
            <div className="absolute" style={{ top: '86%', left: '184%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">Alert!</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>
            
            {/* #india pg 2 */}
            <div className="absolute" style={{ top: '32.5%', left: '168%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">
                3 events of High Severity
              </div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>
          </div>
          </div>

          {/* Second Map (Duplicate) */}
          <div 
            className="h-full flex-1 bg-cover bg-no-repeat bg-center"
            style={{ backgroundImage: "url('/images/hmm.jpeg')" }}
          >
            {/* Red Dots for second map - same dots, adjusted positions */}
            {/* #canada pg 1 */}
            <div className="absolute" style={{ top: '9.5%', left: '118%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">3 events of High Severity</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>

            {/* #singapore pg 1 */}
            <div className="absolute" style={{ top: '58.9%', left: '76.1%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">2 events of High Severity</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>

              {/* #malaysia pg 1 */}
            <div className="absolute" style={{ top: '52.6%', left: '79.9%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">Alert!</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>

              {/* #australia pg 1 */}
            <div className="absolute" style={{ top: '85.5%', left: '84%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">Alert!</div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>
            
            {/* #india pg 1 */}
            <div className="absolute" style={{ top: '38.5%', left: '68%' }}>
              <div className="bg-red-600 text-white text-xs px-2 py-1 rounded mb-1 text-center">
                3 events of High Severity
              </div>
              <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Content Area - Fixed on screen */}
      <div className="relative z-10 p-4 flex justify-end">
        <div className="w-full md:w lg:w xl:w">
          <HomeNewsList events={events} />
        </div>
      </div>
    </div>
  );
}
