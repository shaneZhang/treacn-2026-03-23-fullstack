import React from 'react'

const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">关于 QTribe</h3>
            <p className="text-gray-600 text-sm">
              QTribe 是一个现代化的博客社交平台，让您可以分享知识、交流想法、结识志同道合的朋友。
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">快速链接</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-600 hover:text-primary text-sm transition-colors">
                  首页
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-primary text-sm transition-colors">
                  发现文章
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-primary text-sm transition-colors">
                  发布文章
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-primary text-sm transition-colors">
                  关于我们
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">联系我们</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-center">
                <svg className="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                contact@qtribe.com
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                400-123-4567
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} QTribe. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
