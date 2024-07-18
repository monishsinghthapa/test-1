export const AppReducer = (state: any, action: { type: any; payload: any; }) => {
  switch (action.type) {
    case "SET_PAGE_NUMBER":

      return {
        ...state,

        pageNum: action.payload
      };

    case "SET_PDF_URL":

      return {
        ...state,
        fileName: action.payload

      };

    case "SET_QUESTION":

      return {
        ...state,
        question: action.payload

      };
      case "SET_REFRENCE_TEXT":

      return {
        ...state,
        referenceText: action.payload

      };

    default:
      return state;
  }
};
