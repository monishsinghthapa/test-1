"use client";

import "./pdfviewer.css";
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

import React, { useState, useCallback, useEffect, ChangeEvent } from "react";

import { CiCircleChevLeft, CiCircleChevRight } from "react-icons/ci";
import { FaRegTimesCircle } from "react-icons/fa";
import { MdZoomIn, MdZoomOut } from "react-icons/md";

import { Document, Page, pdfjs } from "react-pdf";
//import { appContext } from "../../context/AppContext";
import "@react-pdf-viewer/search/lib/styles/index.css";
import { AppContext } from "@/app/Appcontext/AppContext";

//import worker for react-pdf to work
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
    "pdfjs-dist/build/pdf.worker.min.js",
    import.meta.url
).toString();

function PdfViewer(props: { className: any; pdfurl: any; referenceTextInput: any; pdfname: any; onClose: any }) {
    const [numPages, setNumPages] = useState<number>(NaN);
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [searchTerm, setSearchTerm] = useState<string>("");
    const [scale, setScale] = useState<number>(0.8);
    const [pageContent, setPageContent] = useState<string>("");
    const [highlightedText, setHighlightedText] = useState<string>('');
    const [searchEntered, setSearchEntered] = useState<boolean>(false);

    const [searchFound, setSearchFound] = useState<boolean>(false);

    const { className, pdfurl, referenceTextInput, pdfname, onClose } = props;

    const { state } = React.useContext(AppContext)

    let newPageNumber: number = 0;
    const pageText: string = "";

    useEffect(() => {
        
        handlePageNumberClick(parseInt(state.pageNum));
    }, [state.pageNum]);

    useEffect(() => {
        
    }, [pageNumber]);

    ///navigate to page no. on click
    function handlePageNumberClick(pageNum: number) {

        if (numPages !== undefined && (pageNum > numPages || pageNum < 0)) {
            alert(`pageno.${pageNum} is not available in this pdf`);
            return;
        }
        setPageNumber(pageNum);
    }

    //load pdf
    function handleDocumentLoadSuccess({ numPages }: { numPages: number }) {

        setNumPages(numPages);
        setPageNumber(parseInt(state.pageNum));
    }


    function highlightReferenceText(text: string, references: any[]) {

        const combinedPattern = new RegExp(references.join("|"), "gi");

        return text.replaceAll(
            combinedPattern,
            (match) => `<mark style="background-color:red">${match}</mark>`
        );
    }

    //search Functionality
    function handleInputChange(e: ChangeEvent<HTMLInputElement>) {
        setSearchTerm(e.target.value);
    }

    const handleEnterPress = (e: { key: string; }) => {
        if (e.key === "Enter") {
            setSearchFound(false);
            highlightSearchTerm(pageContent, searchTerm);


        }
    };

    function highlightSearchTerm(text: string, searchTerm: string) {

        const index = text.indexOf(searchTerm);

        if (index === -1) {
            // handlePageChangeOnSearch(); 
            return "";
        } else {
            setSearchFound(true);
            return text.replaceAll(searchTerm, (match) => `<mark style="background-color:yellow">${match}</mark>`);
        }
    }

    function handlePageChangeOnSearch() {
        setPageNumber((prevPageNumber) => {
            if (prevPageNumber < numPages && !searchFound) {
                newPageNumber = prevPageNumber + 1;
            }
            return newPageNumber;
        });
    }

    const textRenderer = useCallback(
        (textItem: { str: string; }) => {

            return highlightSearchTerm(textItem.str, searchTerm)
        },
        [pageNumber, searchTerm]
    );

    function changePage(offset: number) {
        setPageNumber((prevPageNumber) => prevPageNumber + offset);
    }

    function previousPage() {
        changePage(-1);
    }

    function nextPage() {
        changePage(1);
    }

    const handleZoomIn = () => {
        setScale(scale < 2 ? scale + 0.1 : 1);
    };

    const handleZoomOut = () => {
        setScale(scale > 0 ? scale - 0.1 : 1);
    };

    const closePDF = () => {
        onClose();
    }

    return (
        <div className={className}>
            <div className="pdfViewer-function-container">
                <div className="pdf-viewer-title">{pdfname}</div>
                <div className="page-count-container">
                    <button
                        className="page-controller-btn"
                        type="button"
                        disabled={pageNumber <= 1}
                        onClick={previousPage}
                    >
                        <CiCircleChevLeft
                            title="Previous Page"
                            className="page-controller-btn"
                        />
                    </button>
                    <p className="page-number">
                        {pageNumber || (numPages ? 1 : "__")}/{numPages || "__"}
                    </p>
                    <button
                        type="button"
                        className="page-controller-btn"
                        disabled={pageNumber >= numPages}
                        onClick={nextPage}
                    >
                        <CiCircleChevRight
                            title="Next Page"
                            className="page-controller-btn"
                        />
                    </button>
                </div>
                <div className="pdf-icons-container">
                    <MdZoomIn
                        className="pdf-icons"
                        title="zoom in"
                        onClick={handleZoomIn}
                    />
                    <MdZoomOut
                        className="pdf-icons"
                        title="zoom out"
                        onClick={handleZoomOut}
                    />
                    <input
                        className="search-box"
                        type="search"
                        value={searchTerm}
                        onChange={(e) => handleInputChange(e)}
                        onKeyDown={handleEnterPress}
                    />
                    <div style={{ color: 'white', display: 'flex', padding: '5px 0px 5px 9px', alignItems: 'center', cursor: 'pointer' }}  onClick={closePDF}><FaRegTimesCircle /></div>
                </div>
            </div>
            <div className="pdf-container">
                <Document
                    file={pdfurl}
                    onLoadSuccess={handleDocumentLoadSuccess}
                    onLoadError={(error) =>
                        console.log("error while loading pdf", error.message)
                    }
                >
                    <Page
                        pageNumber={pageNumber}
                        customTextRenderer={textRenderer}
                        scale={scale}
                        width={750}
                    />
                </Document>
            </div>
        </div>
    );
}

export default PdfViewer;
