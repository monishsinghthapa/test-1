"use client";

import { CreateMessage, useChat } from "ai/react";
import { ChatInput, ChatMessages } from "./ui/chat";
import PdfViewer from "./ui/pdf";
import { signal } from "@preact/signals-react";
import { URL_DICT } from '../components/ui/pdf/pdfmapping';
import React, { useEffect, useState } from "react";

import { AppContext } from "../Appcontext/AppContext";



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
const onPDFClose = ()=>{
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
    </div>
  );
}
