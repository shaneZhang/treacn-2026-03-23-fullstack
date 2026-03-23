import React, { type ReactNode } from 'react'
import Navbar from './Navbar.tsx'
import Footer from './Footer.tsx'

interface MainLayoutProps {
  children: ReactNode
  showFooter?: boolean
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, showFooter = true }) => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <main className="flex-grow">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  )
}

export default MainLayout
