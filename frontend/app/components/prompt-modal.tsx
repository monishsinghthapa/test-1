import React, { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { CreateMessage, useChat } from 'ai/react';
import { AppContext } from '../Appcontext/AppContext';
import { setQuestion } from '../Appcontext/Action';

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    menuItemData: any; // Adjust the type according to the data structure of your menu item
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, menuItemData }) => {

    const { dispatch } = React.useContext(AppContext)

    useEffect(() => {
        if (menuItemData && !menuItemData.hasOwnProperty('dropdown')) {
            setQuestion(dispatch, menuItemData.prompt)
            onClose();
        }
    }, [menuItemData])


    const modalCss = {
        zIndex: 55
    };
    function ddType(type: string) {
        switch (type) {
            case 'drivers':
                return 'Select Driver'
            case 'quarters':
                return 'Select Quarter'
            case 'fy':
                return 'Select Fiscal Year'
            case 'company':
                    return 'Select Company'

            default:
                break;
        }
    }

    const [selectedDriver, setSelectedValues] = useState<{ [key: string]: string }>({});

    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>, type: string) => {
        setSelectedValues(prevState => ({
            ...prevState,
            [type]: e.target.value,
        }));
    };

    function reframedQues(que: string): string {
        // var que = this.data.promptVar
        // que = que.replace('{{Q}}', this.selectedQuarter)
        // que = que.replace('{{FY}}', this.selectedFY)
        // que = que.replace('{{D}}', selectedDriver) 
        let updatedQue = que;
        if (que) {
            if (selectedDriver.drivers)
                updatedQue = updatedQue.replace('{{D}}', selectedDriver.drivers);
            if (selectedDriver.quarters)
                updatedQue = updatedQue.replace('{{Q}}', selectedDriver.quarters);
            if (selectedDriver.fy)
                updatedQue = updatedQue.replace('{{FY}}', selectedDriver.fy);
            if(selectedDriver.company)
                updatedQue = updatedQue.replace('{{COMP}}',selectedDriver.company)
        }

        return updatedQue;
    }




    function submitQuery() {
        setQuestion(dispatch, reframedQues(menuItemData.promptVar))
        onClose();
        // const userPrompt: CreateMessage = { role: 'user', content: reframedQues(menuItemData.promptVar) };
        // append(userPrompt);
        // console.log(reframedQues(menuItemData.promptVar))
    }
    return (
        <div style={modalCss} className={`fixed  inset-0 flex justify-center items-center bg-gray-800 bg-opacity-50 ${isOpen ? '' : 'hidden'}`}>
            <div className="bg-white p-4 rounded-lg">
                <h2 className="text-xl font-bold mb-2">Generate prompt</h2>
                {menuItemData?.dropdown?.map((item: any, index: number) => (
                    <div key={index} className='mb-2 border rounded'>
                        <div key={index} className="flex justify-between px-2 py-1">
                            <label className="mr-2">{ddType(item.type)}: </label>
                            <select value={selectedDriver[item.type]} onChange={(e) => handleSelectChange(e, item.type)}>
                                <option>Select</option>
                                {item.option.map((option: any, idx: any) => (
                                    <option key={idx} value={option}>{option}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                ))}
                <p>{reframedQues(menuItemData?.promptVar)}</p>

                <div className='flex'>
                    <button onClick={onClose} className="ml-auto mt-4 bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded-md">Close</button>
                    <Button onClick={submitQuery} className="mt-4  ml-2">Submit Query</Button>
                </div>
            </div>
        </div>
    );
}

export default Modal;
