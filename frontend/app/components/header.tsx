import Image from "next/image";

interface HeaderProps {
  toggleDrawer: () => void;
}

const Header: React.FC<HeaderProps> = ({ toggleDrawer }) => {
  return (
    <div className="flex justify-between items-center bg-white shadow-md p-4 w-full grow-0">
      <div className="flex items-center">
        <button onClick={toggleDrawer} className="mr-4 focus:outline-none">
          <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
        </button>
        <img src="/mck_logo.png" alt="Logo" className="h-5" />
        <span className="ml-4 font-bold  text-xl">Fiscal Navigator</span>
      </div>
    </div>
  );
}

export default Header;