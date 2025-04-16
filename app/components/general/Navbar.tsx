"use client"

import Link from "next/link"
import { Search } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar,  AvatarFallback, AvatarImage } from "../ui/avatar"

export default function Navbar() {
  return (
  <>
      <nav className="backdrop-blur-[10px] fixed top-0 left-0 right-0 z-50 mx-2 h-[44px] flex-shrink-0 rounded-b-[21.308px] bg-[rgba(64,61,61,0.56)] flex items-center justify-between px-6 font-inter">
        <div className="flex items-center space-x-4">
          <Link href="/" className="text-white font-bold text-[24px] font-[700] pb-1">EWS</Link>
        </div>
        
        <div className="flex items-center justify-center bg-[rgba(255,255,255,0.3)] rounded-[15.75px] w-[40%] h-[70%] px-3 relative">
            <div className="absolute top-1/2 transform -translate-y-1/2 flex items-center align-center pointer-events-none">
              <Search className="h-4 w-4 text-white search-icon stroke-[2.75]" />
              <span className="text-white font-[700] ml-2 mb-0.5">Search</span>
            </div>
          <input 
            className="absolute bg-transparent border-none outline-none text-white placeholder:text-white text-[16px] font-[600] w-full text-sm text-center placeholder:text-center focus:placeholder:opacity-0"
            
            type="text"
            onFocus={(e) => {
              e.currentTarget.previousElementSibling?.classList.add('hidden');
            }}
            onBlur={(e) => {
              if (e.currentTarget.value === '') {
          e.currentTarget.previousElementSibling?.classList.remove('hidden');
              }
            }}
          />
        </div>
        
        <div className="flex items-center align-right space-x-4 mb-0.5">
        <Avatar>
          <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <span className="text-white font-[700] text-[16px] mb-0.5">Admin</span>
        </div>

      </nav>
      {/* Spacer to prevent content from being hidden under the navbar */}
      <div className="h-[44px] w-full"></div>
  </>)
}



// import { useState } from "react"
// import Link from "next/link"
// import { usePathname } from "next/navigation"
// import { Menu } from "lucide-react"

// import { cn } from "@/lib/utils"
// import { Button } from "@/components/ui/button"
// import {
//   Sheet,
//   SheetContent,
//   SheetTrigger,
// } from "@/components/ui/sheet"

// const navItems = [
//   { label: "Home", href: "/" },
//   { label: "Problems", href: "/problems" },
//   { label: "Contests", href: "/contests" },
//   { label: "Leaderboard", href: "/leaderboard" },
//   { label: "About", href: "/about" },
// ]

// export default function Navbar() {
//   const [open, setOpen] = useState(false)
//   const pathname = usePathname()
  
//   return (
//     <header className="sticky top-0 z-50 w-full border-b bg-background">
//       <div className="container flex h-16 items-center justify-between">
//         <div className="flex items-center gap-2">
//           <Link 
//             href="/" 
//             className="flex items-center space-x-2 font-bold text-xl"
//           >
//             <span>CommonwealthCF</span>
//           </Link>
//         </div>
        
//         {/* Desktop Navigation */}
//         <nav className="hidden md:flex items-center gap-6">
//           {navItems.map((item) => (
//             <Link
//               key={item.href}
//               href={item.href}
//               className={cn(
//                 "text-sm font-medium transition-colors hover:text-primary",
//                 pathname === item.href
//                   ? "text-foreground font-semibold"
//                   : "text-muted-foreground"
//               )}
//             >
//               {item.label}
//             </Link>
//           ))}
//           <Button asChild variant="default" size="sm">
//             <Link href="/sign-in">Sign In</Link>
//           </Button>
//         </nav>
        
//         {/* Mobile Navigation */}
//         <Sheet open={open} onOpenChange={setOpen}>
//           <SheetTrigger asChild className="md:hidden">
//             <Button variant="ghost" size="icon">
//               <Menu className="h-5 w-5" />
//               <span className="sr-only">Toggle menu</span>
//             </Button>
//           </SheetTrigger>
//           <SheetContent side="right">
//             <nav className="flex flex-col gap-4 mt-8">
//               {navItems.map((item) => (
//                 <Link
//                   key={item.href}
//                   href={item.href}
//                   onClick={() => setOpen(false)}
//                   className={cn(
//                     "text-sm font-medium transition-colors hover:text-primary",
//                     pathname === item.href
//                       ? "text-foreground font-semibold"
//                       : "text-muted-foreground"
//                   )}
//                 >
//                   {item.label}
//                 </Link>
//               ))}
//               <Button asChild variant="default" size="sm" className="mt-2">
//                 <Link href="/sign-in">Sign In</Link>
//               </Button>
//             </nav>
//           </SheetContent>
//         </Sheet>
//       </div>
//     </header>
//   )
// }