async function getData(eventID: string) {
    // try {
    //     // Replace this URL with your actual API endpoint
    //     const response = await fetch(`https://your-api.com/events/${eventID}`);
        
    //     if (!response.ok) {
    //         throw new Error(`Failed to fetch event data: ${response.status}`);
    //     }
        
    //     return await response.json();
    // } catch (error) {
    //     console.error('Error fetching event data:', error);
    //     return null;
    // }

    // Mock data for development
    return {
        id: eventID,
        title: "Sample Event Title is here for Event",
        date: "23hrs ago",
        time: "18:00",
        location: "India",
        description: "This is a sample event description for development purposes. It showcases how event data will be displayed on the page.",
        organizer: "Commonwealth Student Organization",
        attendees: 42,
        maxCapacity: 100,
        serevrity: "VERY SEVERE",
        category: "POLTICAL",
        imageUrl: "https://placehold.co/600x400?text=Event+Image",
        timeline: [
            {
                title: "Event Created",
                time: "23 hours ago",
                description: "Event was created by Commonwealth Student Organization"
            },
            {
                title: "First Update",
                time: "12 hours ago",
                description: "Location confirmed as India"
            },
            {
                title: "Second Update",
                time: "8 hours ago",
                description: "Event severity escalated to VERY SEVERE"
            },
            {
                title: "Latest Update",
                time: "2 hours ago",
                description: "42 people have joined"
            }
        ]
    };
}

export default async function EventPage({ params }: { params: { eventID: string } }) {
    const { eventID } = await params;
    const eventData = await getData(eventID);
    
    if (!eventData) {
        return <div>Event not found or error loading event data</div>;
    }

    return (
    <>

        <div> 
            <div>
                {/* Event image and details */}
                <div className="mr-2 ml-2 mt-2 w-[50%] h-auto overflow-y-hidden bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
                <h2 className="mt-2 text-[32px] font-[700] text-white leading-[32px]">{eventData.title}</h2>
                <div className="flex items-center mt-2.5 mb-4">
                    <span className="text-[14px] font-[400] text-white">{eventData.date}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="bg-white font-[775] text-[12px] px-0.5 text-[#5F5C5D]">{eventData.category}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="text-[14px] font-[700] text-white">{eventData.location}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="bg-white font-[775] text-[12px] px-2 text-[#5F5C5D] rounded-[14px]">{eventData.serevrity}</span>
                </div>
                <img 
                className="rounded-[17.617px] object-cover mb-2 align-center"
                src={eventData.imageUrl || ""}
                width={700}
                height={400}
                alt={`${eventData.title} Image`}
                />
                </div>

                <div className="mr-2 ml-2 my-2 w-[50%] h-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
                    <h2 className="mt-2 text-[18px] font-[700] text-white leading-[18px]">Summary</h2>
                    <p className="text-[14px] font-[400] text-white mt-4 mb-2">{eventData.description}</p>
                </div>
            </div>

            {/* Timeline component */}
            <div className="absolute top-11 right-1 mx-2 my-2 w-[48%] h-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
                <h2 className="mt-2 text-[18px] font-[700] text-white leading-[18px]">Timeline</h2>

                <div className="mt-4">
                    {eventData.timeline && eventData.timeline.map((item, index) => {
                        const isFirst = index === 0;
                        const isLast = index === eventData.timeline.length - 1;
                        
                        return (
                            <div key={index} className="flex items-start">
                                <div className="flex flex-col items-center">
                                    <div className="w-3 h-3 bg-white rounded-full"></div>
                                    {!isLast && <div className="w-0.5 h-16 bg-white/30"></div>}
                                </div>
                                <div className="ml-4">
                                    <h3 className="text-white text-[16px] font-semibold">{item.title}</h3>
                                    <p className="text-gray-300 text-sm">{item.time}</p>
                                    <p className="text-white text-sm mt-1">{item.description}</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>

        <div>

        </div>
    </>
    );
}