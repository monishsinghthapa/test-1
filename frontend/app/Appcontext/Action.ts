import { Dispatch } from 'react'
import { ActionType, IAction } from './AppContext'

export const setPageNumber = (dispatch: Dispatch<IAction>, param: any) => {


    dispatch({ type: ActionType.SET_PDF_URL, payload: param.file_name })
    dispatch({ type: ActionType.SET_PAGE_NUMBER, payload: param.page_label })

}

export const setQuestion = (dispatch: Dispatch<IAction>, param: any) => {

    console.log(param)
    dispatch({ type: ActionType.SET_QUESTION, payload: param })


}

