import { createContext, useContext, ReactNode, useState, useReducer, Dispatch } from "react";
import { AppReducer } from "./Appreducer";

export type IAction = {
    type: ActionType,
    payload: any

}

export enum ActionType {
    SET_PAGE_NUMBER = 'SET_PAGE_NUMBER',
    SET_PDF_URL = 'SET_PDF_URL',
    SET_QUESTION = 'SET_QUESTION',
    SET_REFRENCE_TEXT = 'SET_REFRENCE_TEXT'


}
export interface IAppState {
    fileName: string,
    pageNum: string,
    question: string,
    referenceText:string
}
type appContextType = {
    state: IAppState
    dispatch: React.Dispatch<IAction>
};
export const initialState: IAppState = {
    fileName: '',
    pageNum: '',
    question: '',
    referenceText:''
}

const appContextDefaultValues: appContextType = {
    state: {
        fileName: '',
        pageNum: '',
        question: "",
        referenceText:''
    },
    dispatch: () => { }
};

export const AppContext = createContext<appContextType>(appContextDefaultValues);



type Props = {
    children: ReactNode;
};

export function AppProvider({ children }: Props) {

    const [state, dispatch] = useReducer(AppReducer, appContextDefaultValues);


    const value = {
        state,
        dispatch
    };

    return (
        <>
            <AppContext.Provider value={value}>
                {children}
            </AppContext.Provider>
        </>
    );
}