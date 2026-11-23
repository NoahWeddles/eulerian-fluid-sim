import { useEffect, useRef } from "react"
import { drawGrid, useGrid, mouseToCell } from "./Grid"

export default function App() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { grid, setCellColor } = useGrid(20, 20, 20, 20);


    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        drawGrid(ctx, grid);
    }, [grid]);
    return (
        <>
        <div className="w-full h-screen bg-emerald-700">
        <canvas ref={canvasRef} width={500} height={500} onClick={(e)=>{
                    const cell = mouseToCell(grid, canvasRef.current, e.clientX, e.clientY);
                    if (cell) setCellColor(cell.row, cell.col, "red");
        }} 
        onContextMenu={(e) => {
            const cell = mouseToCell(grid, canvasRef.current, e.clientX, e.clientY);
            if (cell) {setCellColor(cell.row, cell.col, "green")
                setCellColor(cell.row+1, cell.col, "green")
                setCellColor(cell.row-1, cell.col, "green")
                setCellColor(cell.row, cell.col+1, "green")
                setCellColor(cell.row, cell.col-1, "green")
            };
        }}/>
        </div>
        </>
    )
}
