"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import Image from "next/image"
import active from "@/public/active.svg"
import allnews from "@/public/allnews.svg"
import potential from "@/public/potential.svg"

export interface Event {
    imageUrl: string;
    title: string;
    category: string;
    location: string;
    severity: string;
    type: string; // 'active' or 'potential'
}

interface EventProps {
    event: {
        imageUrl: string;
        title: string;
        category: string;
        location: string;
        severity: string;
    }
}

export function EventComponent({ event }: EventProps) {
    return (
        <div className="flex items-start my-4">
            <div className="relative w-[80px] h-[80px] rounded-full bg-gray-300 ml-2 mr-4 flex-shrink-0 overflow-hidden">
                <Image 
                    src={event.imageUrl || ""}
                    alt={event.title}
                    fill // Use fill property instead of width/height
                    className="object-cover" // object-cover ensures the image maintains aspect ratio
                    sizes="80px" // Hint for the browser about the image size
                />
            </div>
            <div className="flex flex-col">
                <h2 className="mt-[4] text-[21px] font-[700] text-white leading-[21px]">{event.title}</h2>
                <div className="flex items-center gap-2 mt-1">
                    <span className="bg-white font-[775] text-[12px] px-0.5 text-[#5F5C5D]">{event.category}</span>
                    <div className="flex items-center">
                        <div className="w-2 h-2 bg-white rounded-full mr-1"></div>
                        <span className="text-[14px] font-[600] text-white">{event.location}</span>
                    </div>
                    <span className="bg-white font-[775] text-[12px] px-2 text-[#5F5C5D] rounded-[14px]">{event.severity}</span>
                </div>
            </div>
        </div>
    )
}

interface HomeNewsListProps {
    events: Event[];
}

export default function HomeNewsList({ events }: HomeNewsListProps) {
    // Filter events by type
    const activeEvents = events.filter(event => event.type === 'active');
    const potentialEvents = events.filter(event => event.type === 'potential');
    // All events will be displayed in the "All" tab

    return (
        <Tabs defaultValue="Potential">
            <TabsList className="ml-auto mr-2 mt-4 w-[25%] h-[7.5vh] bg-[rgba(64,61,61,0.56)] rounded-[17.617px] backdrop-blur-[10px]">
                <TabsTrigger value="Active" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div>
                        <Image src={active} alt="Active" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>Active</span>
                </TabsTrigger>
                <TabsTrigger value="Potential" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div>
                        <Image src={potential} alt="Potential" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>Potential</span>
                </TabsTrigger>
                <TabsTrigger value="All" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div>
                        <Image src={allnews} alt="AllNews" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>All News</span>
                </TabsTrigger>
            </TabsList>

            <TabsContent value="Active" className="ml-auto mr-2 mt-1 w-[25%] h-auto max-h-[70vh] overflow-y-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-1 backdrop-blur-[10px]">
                <div className="ml-4 font-[800] text-white text-sm mt-8 mb-4">TOP EVENTS</div>
                {activeEvents.length > 0 ? (
                    <>
                        {activeEvents.slice(0, 4).map((event, index) => (
                            <EventComponent key={index} event={event} />
                        ))}
                        <div className="text-center mb-5">
                            <button className="bg-[rgba(255,255,255,0.3)] text-white font-[700] py-1.5 px-4 rounded-lg hover:bg-[rgba(255,255,255,0.4)] transition-colors">
                                View More
                            </button>
                        </div>
                    </>
                ) : (
                    <div className="text-white text-center py-4">No active events</div>
                )}
            </TabsContent>

            <TabsContent value="Potential" className="ml-auto mr-2 mt-1 w-[25%] h-auto max-h-[70vh] overflow-y-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-1 backdrop-blur-[10px]">
                <div className="ml-4 font-[800] text-white text-sm mt-8 mb-4">TOP EVENTS</div>
                {potentialEvents.length > 0 ? (
                    <>
                        {potentialEvents.slice(0, 4).map((event, index) => (
                            <EventComponent key={index} event={event} />
                        ))}
                        <div className="text-center mb-5">
                            <button className="bg-[rgba(255,255,255,0.3)] text-white font-[700] py-1.5 px-4 rounded-lg hover:bg-[rgba(255,255,255,0.4)] transition-colors">
                                View More
                            </button>
                        </div>
                    </>
                ) : (
                    <div className="text-white text-center py-4">No potential events</div>
                )}
            </TabsContent>

            <TabsContent value="All" className="ml-auto mr-2 mt-1 w-[25%] h-auto max-h-[70vh] overflow-y-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-1 backdrop-blur-[10px]">
                <div className="ml-4 font-[800] text-white text-sm mt-8 mb-4">TOP EVENTS</div>
                {events.length > 0 ? (
                    <>
                        {events.slice(0, 4).map((event, index) => (
                            <EventComponent key={index} event={event} />
                        ))}
                        <div className="text-center mb-5">
                            <button className="bg-[rgba(255,255,255,0.3)] text-white font-[700] py-1.5 px-4 rounded-lg hover:bg-[rgba(255,255,255,0.4)] transition-colors">
                                View More
                            </button>
                        </div>
                    </>
                ) : (
                    <div className="text-white text-center py-4">No events</div>
                )}
            </TabsContent>
        </Tabs>
    )
}