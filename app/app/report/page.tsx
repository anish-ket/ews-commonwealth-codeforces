'use client';

import Image from "next/image"
import active from "@/public/active.svg"
import allnews from "@/public/allnews.svg"
import potential from "@/public/potential.svg"
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useState } from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { ChevronDown, Globe, X, FileText, Bell, AlertTriangle, CalendarIcon } from 'lucide-react';
import { addDays,format } from "date-fns"
import { cn } from "@/lib/utils"
import { DateRange } from "react-day-picker"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import React from "react";
import { Bar, BarChart, CartesianGrid, LabelList, XAxis } from "recharts"
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";



const regions = ["World", "Global", "Europe", "Asia", "Americas", "Africa"];
const types = ["All Types", "Articles", "Reports", "Press Releases", "Interviews"];


export default function ReportPage() {
  // States for filters
  const [activeFilter, setActiveFilter] = useState(false);
  const [potentialFilter, setPotentialFilter] = useState(true);
  const [allNewsFilter, setAllNewsFilter] = useState(true);
  const [date, setDate] = React.useState<DateRange | undefined>({
    from: new Date(2022, 0, 20),
    to: addDays(new Date(2022, 0, 20), 20),
  })

  const [region, setRegion] = useState("World");

  const [contentType, setContentType] = useState("All Types");
  
  const newsItems = [
    {
      title: "Canada imposes 25% tarrifs in trade war with US",
      description: "China called the vessel's downing an excessive reaction and said it retains the right to respond further",
      category: "POLITICAL",
      country: "Canada",
      severity: "VERY EXTREME",
      date: "3 hrs ago"
    },
    {
      title: "Russia-Ukriane war live: arming Ukriane is 'only path to peace'.",
      description: "The British foreign secretary, James Cleverly, said Helping to arm Ukraine so it can defend itself is the swiftest path to achieving peace.",
      category: "MILITARY",
      country: "UK",
      severity: "VERY EXTREME",
      date: "7 hrs ago"
    },
    {
      title: "Is TikTok really giving your data to China?",
      description: "TikTok is owned by Beijing-based ByteDance. In China, the government censors the internet and users online surveillance to control people.",
      category: "MILITARY",
      country: "USA",
      severity: "VERY EXTREME",
      date: "12 hrs ago"
    }
  ];


  
  const chartData1 = [
    { month: "January", verySevereEvents: 4 },
    { month: "February", verySevereEvents: 5 },
    { month: "March", verySevereEvents: 2 },
    { month: "April", verySevereEvents: 9 },
    { month: "May", verySevereEvents: 2 },
    { month: "June", verySevereEvents: 4 },
  ]

  const chartConfig1 = {
    desktop: {
      label: "Very Severe Events",
      color: "white",
    },
  } satisfies ChartConfig

  function handleFilterChange(filterType: string) {
    switch (filterType) {
      case 'active':
        setActiveFilter(true);
        setPotentialFilter(false);
        setAllNewsFilter(false);
        break;
      case 'potential':
        setActiveFilter(false);
        setPotentialFilter(true);
        setAllNewsFilter(false);
        break;
      case 'all':
        setActiveFilter(false);
        setPotentialFilter(false);
        setAllNewsFilter(true);
        break;
      default:
        break;
    }
  }

  function handleClearFilter(){
    setActiveFilter(true);
    setPotentialFilter(false);
    setAllNewsFilter(false);
    setRegion("World");
    setContentType("All Types")
  }

  return (
    

    <main className="min-h-screen text-white p-4">

            <div 
            className="fixed top-0 left-0 w-full h-full z-[-1]"
            style={{
                backgroundImage: "url('/images/backgrounds/event-bg.jpeg')",
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                filter: "blur(15px) brightness(0.9)"
            }}
            />
      {/* Filter Bar */}
      <div className="flex flex-wrap items-center gap-13 mb-6">
        {/* Left side filters */}
        <Tabs defaultValue="Potential">
            <TabsList className="ml-auto mr-2 w-[100%] h-[8vh] bg-[rgba(64,61,61,0.56)] rounded-[17.617px] backdrop-blur-[10px]">
                <TabsTrigger value="Active" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div onClick={() => handleFilterChange('active')}>
                        <Image src={active} alt="Active" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>Active</span>
                </TabsTrigger>
                <TabsTrigger value="Potential" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div onClick={() => handleFilterChange('potential')}>
                        <Image src={potential} alt="Potential" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>Potential</span>
                </TabsTrigger>
                <TabsTrigger value="All" className="data-[state=active]:bg-[rgba(255,255,255,0.3)] data-[state=active]:font-[700] rounded-[17.951px] data-[state=active]:text-white transition-colors text-white font-[700]">
                    <div onClick={() => handleFilterChange('all')}>
                        <Image src={allnews} alt="AllNews" className="w-[24px] h-[24px] mt-0.5"/>
                    </div>
                    <span>All News</span>
                </TabsTrigger>
            </TabsList>
        </Tabs>
        {/* <TabsContent value="Active">{setActiveFilter(true)}</TabsContent> */}

        <div className="flex gap-4">
                <div className="rounded-[17.951px]">
                <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" className="bg-[rgba(64,61,61,0.56)] font-[700] text-white py-7 px-4 flex items-center gap-2 rounded-[17.617px]">
                <Globe size={16} className="mr-2" />
                {region}
                <ChevronDown size={14} className="ml-2" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="">
                {regions.map((item) => (
                <DropdownMenuItem 
                    key={item} 
                    className="cursor-pointer"
                    onClick={() => setRegion(item)}
                >
                    {item}
                </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
            </DropdownMenu>
                </div>

                <div className="rounded-[17.951px]">
                <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" className="bg-[rgba(64,61,61,0.56)] text-white py-7 px-4 rounded-[17.617px] flex items-center gap-2 font-[700]">
                <FileText size={16} className="mr-2" />
                {contentType}
                <ChevronDown size={14} className="ml-2" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="">
                {types.map((item) => (
                <DropdownMenuItem 
                    key={item} 
                    className=" cursor-pointer"
                    onClick={() => setContentType(item)}
                >
                    {item}
                </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
            </DropdownMenu>
                </div>

            <div>
            <Popover>
            <PopoverTrigger asChild>
            <Button
            id="date"
            variant={"outline"}
            className={cn(
              "rounded-[17.617px] w-[265px] justify-start text-left bg-[rgba(64,61,61,0.56)] text-white py-7 font-[700]",
              !date && "text-white"
            )}
            >
            <CalendarIcon className="mr-2" />
            {date?.from ? (
              date.to ? (
                <>
              {format(date.from, "LLL dd, y")} -{" "}
              {format(date.to, "LLL dd, y")}
              
              </>
              ) : (
                format(date.from, "LLL dd, y")
              )
            ) : (
              <span>Pick a date</span>
            )}
            <ChevronDown size={14} className="ml-auto" />
            </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0 " align="start">
            <Calendar
            initialFocus
            mode="range"
            defaultMonth={date?.from}
            selected={date}
            onSelect={setDate}
            numberOfMonths={2}
            />
            </PopoverContent>
            </Popover>
            </div>
        </div>

        {/* Clear Filters button */}
        <button 
          className="bg-[rgba(64,61,61,0.56)] px-4 py-2 rounded-lg h-[7vh] hover:bg-[rgba(255,255,255,0.9)] hover:text-black hover:border-[0.5] hover:border-black flex items-center gap-2 font-[700] text-white rounded-[17.617px]"
          onClick={handleClearFilter}
          >
          <X size={20} className="mr-2" />
          <span className="text-sm">Clear Filters</span>
        </button>
      </div>
      
      {/* News Cards */}
      <div className="flex flex-col gap-4 w-[65%]">
        {newsItems.map((item, index) => (
          <div key={index} className="bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-6.5 py-6.5 backdrop-blur-[10px] flex gap-4">
            <div className="w-24 h-24 rounded-full bg-gray-300"></div>
            <div className="flex-1">
              <a href="/event/1"><h2 className="text-2xl font-bold mb-2">{item.title}</h2></a>
              <p className="text-sm mb-3">{item.description}</p>
              <div className="flex items-center mt-2.5 mb-4">
                    <span className="text-[14px] font-[400] text-white">{item.date}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="bg-white font-[775] text-[12px] px-0.5 text-[#5F5C5D]">{item.category}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="text-[14px] font-[700] text-white">{item.country}</span>
                    <div className="w-1.5 h-1.5 bg-white rounded-full mx-1 mt-0.5"></div>
                    <span className="bg-white font-[775] text-[12px] px-2 text-[#5F5C5D] rounded-[14px]">{item.severity}</span>
                </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Generate Report Button */}
      <div className="absolute top-33.5 right-1 mx-2 my-2 w-[33%] h-auto bg-[rgba(64,61,61,0.56)] rounded-[17.617px] px-6.5 py-5 backdrop-blur-[10px]">
        <h2 className="mt-2 text-[18px] font-[700] text-white leading-[18px]">Slected News Stats</h2><Button className="absolute top-5 right-5 bg-white text-black hover:bg-gray-200">Generate Report</Button>
        
        <br /><br />

        <h3 className="text-[16px] font-[700] text-white leading-[18px]">Very Severe Events Distribution</h3><br />
        <ChartContainer config={chartConfig1}>
          <BarChart
            accessibilityLayer
            data={chartData1}
            margin={{
              top: 20,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="month"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              className="font-[700] text-white"
              tickFormatter={(value) => value.slice(0, 3)}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Bar dataKey="verySevereEvents" fill="var(--color-desktop)" radius={8}>
              <LabelList
          position="top"
          offset={12}
          fill="white"
          fontSize={12}
          fontWeight={700}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
        
      
      </div>
    </main>
  );
}
