"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { 
  Sheet, 
  SheetContent, 
  SheetTrigger 
} from "@/components/ui/sheet"
import { 
  Home, 
  ListOrdered, 
  Users, 
  Award, 
  BookOpen, 
  Settings,
  Code 
} from "lucide-react"

export function Sidebar() {
  const [open, setOpen] = useState(false)
  const pathname = usePathname()

  const routes = [
    {
      name: "Home",
      path: "/dashboard",
      icon: <Home className="h-5 w-5 mr-3" />
    },
    {
      name: "News List",
      path: "/report",
      icon: <Code className="h-5 w-5 mr-3" />
    },
    {
      name: "Country Dashboard",
      path: "/countrydashboard",
      icon: <ListOrdered className="h-5 w-5 mr-3" />
    },
    // {
    //   name: "Leaderboard",
    //   path: "/leaderboard",
    //   icon: <Award className="h-5 w-5 mr-3" />
    // },
    // {
    //   name: "Community",
    //   path: "/community",
    //   icon: <Users className="h-5 w-5 mr-3" />
    // },
    // {
    //   name: "Learning",
    //   path: "/learning",
    //   icon: <BookOpen className="h-5 w-5 mr-3" />
    // },
    {
      name: "Settings",
      path: "/settings",
      icon: <Settings className="h-5 w-5 mr-3" />
    }
  ]

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <div 
          className="fixed left-0 top-1/2 -translate-y-1/2 z-50 h-[150px] w-[10px] bg-[rgba(64,61,61,0.56)] rounded-r-[17.617px] backdrop-blur-[10px] flex items-center justify-center cursor-pointer"
          onClick={() => setOpen(true)}
        />
      </SheetTrigger>
      
      <SheetContent side="left" className="w-[250px] sm:w-[300px] p-0">
        <div className="flex flex-col h-full">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold">Commonwealth</h2>
            <p className="text-sm text-muted-foreground">Codeforces Portal</p>
          </div>
          
          <nav className="flex-1 p-4">
            <ul className="space-y-2">
              {routes.map((route) => (
                <li key={route.path}>
                  <Link 
                    href={route.path}
                    className={`flex items-center p-3 rounded-md hover:bg-secondary transition-colors ${
                      pathname === route.path ? "bg-secondary font-medium" : ""
                    }`}
                    onClick={() => setOpen(false)}
                  >
                    {route.icon}
                    <span>{route.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
          
          <div className="p-4 mt-auto border-t">
            <div className="flex items-center">
              <div className="w-8 h-8 rounded-full bg-primary mr-3" />
              <div>
                <p className="text-sm font-medium">User Profile</p>
                <p className="text-xs text-muted-foreground">Sign Out</p>
              </div>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}

export default Sidebar
