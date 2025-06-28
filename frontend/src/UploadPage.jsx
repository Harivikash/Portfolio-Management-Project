import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [toast, setToast] = useState({ show: false, message: "", type: "" });
  const [loading, setLoading] = useState(false);

  const showToast = (message, type = "success") => {
    setToast({ show: true, message, type });
    setTimeout(() => {
      setToast({ show: false, message: "", type: "" });
    }, 4000);
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      showToast("Please select a CSV file.", "danger");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        showToast("CSV uploaded successfully!", "success");
      } else {
        showToast("Upload failed.", "danger");
      }
    } catch (error) {
      console.error(error);
      showToast("Error occurred while uploading.", "danger");
    } finally {
      setLoading(false);
    }
  };

  const handleClearDatabase = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to delete all transactions?"
    );
    if (!confirmed) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/clear_transactions", {
        method: "DELETE",
      });

      if (response.ok) {
        showToast("All transactions deleted successfully.", "success");
      } else {
        showToast("Failed to delete transactions.", "danger");
      }
    } catch (error) {
      console.error(error);
      showToast("Error occurred while clearing transactions.", "danger");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Upload CSV</h2>
      <div className="mb-3">
        <input
          type="file"
          className="form-control"
          accept=".csv"
          onChange={handleFileChange}
          disabled={loading}
        />
      </div>
      <button
        className="btn btn-primary me-3"
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? (
          <>
            <span
              className="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            Uploading...
          </>
        ) : (
          "Upload CSV"
        )}
      </button>

      <button
        className="btn btn-danger"
        onClick={handleClearDatabase}
        disabled={loading}
      >
        {loading ? (
          <>
            <span
              className="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            Deleting...
          </>
        ) : (
          "Delete All Transactions"
        )}
      </button>

      {toast.show && (
        <div
          className={`toast align-items-center text-bg-${toast.type} border-0 position-fixed bottom-0 end-0 m-4 show`}
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          style={{ zIndex: 9999 }}
        >
          <div className="d-flex">
            <div className="toast-body">{toast.message}</div>
            <button
              type="button"
              className="btn-close btn-close-white me-2 m-auto"
              onClick={() => setToast({ show: false, message: "", type: "" })}
            ></button>
          </div>
        </div>
      )}
    </div>
  );
}
