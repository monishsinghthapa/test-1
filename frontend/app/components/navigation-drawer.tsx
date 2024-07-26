import React, { useEffect, useState } from 'react';
import Modal from './prompt-modal';
import { MdHeight } from 'react-icons/md';

interface MenuItem {
    prompt: string
    promptVar: string;
    dropdown: PromptDropDown[]
}
interface PromptDropDown {
    type: string
    option: []
}

interface NavigationDrawerProps {
    isOpen: boolean;
    onClose: () => void;
    handleMenuItemClick: (menuItem: MenuItem) => void;
}

const NavigationDrawer: React.FC<NavigationDrawerProps> = ({ isOpen, onClose, handleMenuItemClick }) => {

    const [menuItems, setMenuItems] = useState<MenuItem[]>([]);

    useEffect(() => {
        const fetchMenuItems = async () => {
            try {
                const response = await fetch('/prompts.json');
                if (!response.ok) {
                    throw new Error('Failed to fetch menu items');
                }
                const data = await response.json();
                setMenuItems(data);
            } catch (error) {
                console.error('Error fetching menu items:', error);
            }
        };

        fetchMenuItems();
    }, []);




    return (
        <div className={`fixed inset-y-0 left-0 bg-white flex flex-col justify-between items-en z-50 w-96  py-6 transform transition-transform ease-in-out duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>

            <div style={{overflowY: "auto"}} >
                <div className='px-4 flex items-center'>
                    <img src="/library.png" style={{ height: '25px' }} />
                    <span className='font-semibold text-xl ml-2'>Prompt Library</span>
                    <button onClick={onClose} className="ml-auto focus:outline-none">
                        <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <ul className='mt-8'>
                    {menuItems.map((item, idx: any) => (
                        <li onClick={() => {
                            console.log(item)
                            handleMenuItemClick(item);
                            onClose(); // Call onClose() here
                        }}
                            className='py-2 px-4 hover:bg-gray-200 cursor-pointer transition-colors duration-300' key={idx}>{item.prompt}</li>
                    ))}
                </ul>
            </div>
            <div className='flex items-center px-4'>
                <span>Powered By </span><img src="/exl.jpg" style={{ height: '30px' }} />
            </div>

        </div>
    );
}

export default NavigationDrawer;
