@echo off
REM ============================================================
REM  تشغيل برنامج إعداد دراسات الجدوى على Windows
REM  Run Feasibility Study App on Windows
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================================
echo   برنامج إعداد دراسات الجدوى - تشغيل تلقائي
echo   Feasibility Study Builder - Auto Run
echo ============================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if errorlevel 1 (
    echo [خطأ] Node.js غير مثبت. يرجى تثبيته من: https://nodejs.org
    echo [Error] Node.js is not installed. Install from: https://nodejs.org
    pause
    exit /b 1
)

REM Check if .env exists; if not, create from example
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [OK] تم إنشاء ملف .env
    ) else (
        echo DATABASE_URL="file:./db/custom.db" > .env
        echo [OK] تم إنشاء ملف .env
    )
)

REM Install dependencies if needed
if not exist "node_modules" (
    echo [1/3] تثبيت الحزم... Installing dependencies...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo [خطأ] فشل تثبيت الحزم
        pause
        exit /b 1
    )
) else (
    echo [1/3] الحزم مثبتة مسبقاً. Dependencies already installed.
)

REM Setup database
echo [2/3] إعداد قاعدة البيانات... Setting up database...
call npx prisma db push
call npx prisma generate

REM Start dev server
echo [3/3] تشغيل التطبيق... Starting app...
echo.
echo ============================================================
echo   ✅ التطبيق يعمل على: http://localhost:3000
echo   افتح المتصفح على هذا الرابط
echo   لإيقاف التطبيق: اضغط Ctrl+C في هذه النافذة
echo ============================================================
echo.

call npm run dev

pause
