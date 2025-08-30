import React from 'react'

interface LayoutProps {
    child: React.ReactNode;
}

export default function Layout({ child }: LayoutProps) {
  return (
    <div>{child}</div>
  )
}
