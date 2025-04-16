import HomeNewsList from "@/components/general/HomeNewsList";
import { Event } from "../components/general/HomeNewsList"; // Import the custom Event type

async function getEventsData(): Promise<Event[]> {
  // This function can be used to fetch or generate event data
  return [
    // Active events
    {
      imageUrl: "/images/floods/kerala-2023.jpg",
      title: "Kerala Flood Emergency",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "High",
      type: "active",
    },
    {
      imageUrl: "/images/cyclones/cyclone-mocha.jpg",
      title: "Cyclone Mocha Relief",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "High",
      type: "active",
    },
    {
      imageUrl: "/images/drought/maharashtra-drought.jpg",
      title: "Maharashtra Drought Response",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Medium",
      type: "active",
    },
    {
      imageUrl: "/images/landslides/himachal-landslide.jpg",
      title: "Himachal Landslide Recovery",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "High",
      type: "active",
    },
    // Potential events
    {
      imageUrl: "/images/monsoon/monsoon-prediction.jpg",
      title: "Monsoon Flood Alert",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Medium",
      type: "potential",
    },
    {
      imageUrl: "/images/heatwave/delhi-heatwave.jpg",
      title: "Delhi Heatwave Warning",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Medium",
      type: "potential",
    },
    {
      imageUrl: "/images/avalanche/sikkim-snowfall.jpg",
      title: "Sikkim Avalanche Risk",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Low",
      type: "potential",
    },
    {
      imageUrl: "/images/earthquake/prediction-zone.jpg",
      title: "Seismic Activity Monitoring",
      category: "ENVIRONMENTAL",
      location: "India",
      severity: "Low",
      type: "potential",
    }
  ];
}

export default async function Home() {
  // Create an empty array or fetch actual events
  const events: Event[] = await getEventsData();
  
  return (
  <div>
    <HomeNewsList events={events} />   
  </div>
  );
}
