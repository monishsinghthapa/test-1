'use client';
import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";
import React, { useRef, useState } from "react";
import NavigationDrawer from "./components/navigation-drawer";
import Modal from "./components/prompt-modal";
import { AppContext, AppProvider } from "./Appcontext/AppContext";
import { setQuestion } from "./Appcontext/Action";

//export const dynamic = "force-dynamic";

export default function Home() {


  const [isDrawerOpen, setIsDrawerOpen] = React.useState(false);
  const [selectedMenuItem, setSelectedMenuItem] = useState<any>(null);


  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const { dispatch } = React.useContext(AppContext)

  const handleMenuItemClick = (menuItem: any) => {
    // if (menuItem.hasOwnProperty('dropdown')) {
    setSelectedMenuItem(menuItem);
    // } else {
    //   console.log(menuItem.prompt)
    //   setQuestion(dispatch, menuItem.prompt)
    // }
  };

  const closeModal = () => {
    setSelectedMenuItem(null);
  };


  return (
    <AppProvider>
      <main className="flex min-h-screen flex-col   gap-2 bg-slate-50">
        <Header toggleDrawer={toggleDrawer} />
        <ChatSection />

      </main>
      {isDrawerOpen && (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-75 z-50" onClick={toggleDrawer}></div>
      )}
      <NavigationDrawer isOpen={isDrawerOpen} onClose={toggleDrawer} handleMenuItemClick={handleMenuItemClick} />
      <Modal isOpen={selectedMenuItem !== null} onClose={closeModal} menuItemData={selectedMenuItem} />
    </AppProvider>
  );
}
