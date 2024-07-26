"use client";

import { CreateMessage, useChat } from "ai/react";
import { AnnotationData, ChatInput, ChatMessages, MessageAnnotation } from "./ui/chat";
import PdfViewer from "./ui/pdf";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { URL_DICT } from '../components/ui/pdf/pdfmapping';
import React, { useEffect, useState } from "react";

import { AppContext } from "../Appcontext/AppContext";
import { JSONValue } from "ai";



export default function ChatSection() {
  const {
    messages,
    input,
    isLoading,
    handleSubmit,
    handleInputChange,
    reload,
    append,
    stop,
  } = useChat({
    api: process.env.NEXT_PUBLIC_CHAT_API,
    headers: {
      "Content-Type": "application/json", // using JSON because of vercel/ai 2.2.26
    },
    onError: (error: unknown) => {
      if (!(error instanceof Error)) throw error;
      const message = JSON.parse(error.message);
      alert(message.detail);
    },
  });
  const [closeModal, setCloseModal] = useState<boolean>(false);
  

  function test(q: string) {
    const userPrompt: CreateMessage = { role: 'user', content: q };
    append(userPrompt);
  }



  const { state } = React.useContext(AppContext)
  useEffect(() => {
    if (state.question && state.question !== '') {
      test(state.question)
    }
  }, [state.question])

  useEffect(() => {
    setCloseModal(!closeModal)
  }, [state.fileName])
  const getPDFUrlFromMapping = (name: any) => {
    if (name !== undefined) {

      return URL_DICT[name]
    }
  }

  useEffect(()=>{
     const annotations = messages[messages.length -1]?.annotations;

    if(annotations !== undefined){
      const value = (annotations[0] as MessageAnnotation).multiple_companies;
      
      if(value){
        toast("Warning: Multi company search may not give good response.")
      }
    } 
  
  },[isLoading])
  const onPDFClose = () => {
    setCloseModal(!closeModal)
  }

  return (
    <div className="flex justify-between grow ml-4 mb-2 ">
      <div className="space-y-4 max-w-[98vw] w-full flex-col ">
        <ChatMessages
          messages={messages}
          isLoading={isLoading}
          reload={reload}
          stop={stop}
        />
        <ChatInput
          input={input}
          handleSubmit={handleSubmit}
          handleInputChange={handleInputChange}
          isLoading={isLoading}
          multiModal={true}
        />
      </div>

      {state.fileName && !closeModal && <div className='w-2/4 bg-white shadow-md mr-4 ml-4 rounded-xl p-4 mb-2 max-h-[82vh]'>
        <PdfViewer
          className={"pdfViewer-container"}
          pdfurl={
            getPDFUrlFromMapping(state.fileName)
          }

          pdfname={state.fileName}
          referenceTextInput={[state.referenceText]}
          onClose={onPDFClose}

        />
      </div>}
      <ToastContainer theme="dark" position="bottom-left" />
    </div>
  );
}
