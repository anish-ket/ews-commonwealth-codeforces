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
        title: "Avoid US Travel",
        date: "23hrs ago",
        time: "18:25",
        location: "Canada",
        description: "An advocacy group representing Canada’s university and college professors is strongly urging academic staff to avoid non-essential travel to the U.S. amid an evolving political landscape, The Canadian Association of University Teachers (CAUT), a group of independent associations and trade unions that represent 72,000 teachers, researchers and other staff at 120 universities and colleges, issued its updated travel advice on Tuesday. CAUT strongly recommends that academic staff travel to the U.S. only if essential and necessary, the warning reads.The organization said that academics who fall into certain categories should exercise particular caution.Those categories include citizens or residents of a country identified as likely to be subject to a travel ban, those from a country that has diplomatic tensions with the U.S., people who expressed negative opinions about the Trump administration or its policies, and those whose research could be seen as at odds with the current U.S. government.Story continues below advertisementThe warning also applies to travellers with passport stamps related to recent travel to countries that may be subject to a travel ban or have diplomatic tensions, and teachers or staff who identify as transgender or whose travel documents indicate a sex other than their sex at birth.2:15 Washington State border towns beg Canadians to come backIf teachers and other staff need to travel, the association also urges them to carefully consider what information they have or need to have on their electronic devices when crossing borders and to take action to protect sensitive information where necessary.Get daily National news Get the day top news, political, economic, and current affairs headlines, delivered to your inbox once a day. Sign up for daily National newsletter Sign Up By providing your email address, you have read and agree to Global News Terms and Conditions and Privacy Policy.",
        organizer: "Commonwealth Student Organization",
        attendees: 42,
        maxCapacity: 100,
        serevrity: "HIGH SEVERITY",
        category: "POLTICAL",
        imageUrl: "/images/events/canada1.jpeg",
        timeline: [
            {
                title: "Avoid U.S. travel if possible, Canadian academics are being urged",
                time: "23 hours ago",
                description: "Canadian university and college professors, as well as other staff at these institutions, are being encouraged to avoid all non-essential travel to the U.S.",
                link:"https://globalnews.ca/news/11132827/us-travel-warning-canadian-academics/"
            },
            {
                title: "Canadian university teachers warned against travelling to the United States",
                time: "22 hours ago",
                description: "Advice includes researchers 'at odds with the position of the current U.S. administration'",
                link:"https://www.cbc.ca/news/canada/travel-warning-united-states-1.7510877"
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
        {/* Background image with blur and reduced brightness */}
        <div 
            className="fixed top-0 left-0 w-full h-full z-[-1]"
            style={{
                backgroundImage: "url('/images/backgrounds/event-bg.jpeg')",
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                filter: "blur(8px) brightness(0.5)"
            }}
        />

        {/* Content container - add opacity to make content stand out better */}
        <div className="relative z-10"> 
            <div>
                {/* Event image and details */}
                <div className="mr-2 ml-2 mt-2 w-[50%] h-auto overflow-y-hidden bg-[rgba(64,61,61,0.76)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
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

                <div className="mr-2 ml-2 my-2 w-[50%] h-auto bg-[rgba(64,61,61,0.76)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
                    <h2 className="mt-2 text-[18px] font-[700] text-white leading-[18px]">Summary</h2>
                    <p className="text-[14px] font-[400] text-white mt-4 mb-2">{eventData.description}</p>
                </div>
            </div>

            {/* Timeline component - increase opacity slightly for better readability */}
            <div className="absolute top-11 right-1 mx-2 my-2 w-[48%] h-auto bg-[rgba(64,61,61,0.76)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
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
                                    <p className="text-gray-300 text-sm mt-1">{item.link}</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    </>
    );
}