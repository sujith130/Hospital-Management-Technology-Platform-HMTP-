import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/Schedule.css';

const DoctorSchedule = () => {
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState('');
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const res = await api.get('/doctors/');
        setDoctors(res.data);
        if (res.data.length > 0) setSelectedDoctorId(res.data[0].id);
      } catch (error) {
        console.error("Fetch Doctors Error:", error);
      }
    };
    fetchDoctors();
  }, []);

  const fetchSchedule = async (doctorId) => {
    if (!doctorId) return;
    setLoading(true);
    try {
      // For demo, we just list potential slots and check availability from doctor model
      const res = await api.get(`/doctors/${doctorId}`);
      const doctor = res.data;
      const times = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00'];

      // Basic check: if slot is within any of the doctor's availability windows
      const processedSlots = times.map(t => {
        const isAvail = doctor.availabilities.some(a => {
          const [h, m] = t.split(':');
          const [sh, sm] = a.start_time.split(':');
          const [eh, em] = a.end_time.split(':');
          const slotMin = parseInt(h) * 60 + parseInt(m);
          const startMin = parseInt(sh) * 60 + parseInt(sm);
          const endMin = parseInt(eh) * 60 + parseInt(em);
          return slotMin >= startMin && slotMin < endMin;
        });
        return { id: t, time: t, status: isAvail ? 'available' : 'unavailable' };
      });
      setSlots(processedSlots);
    } catch (error) {
      console.error("Fetch Schedule Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedule(selectedDoctorId);
  }, [selectedDoctorId]);

  const handleSlotClick = (slot) => {
    if (slot.status !== 'available') return;
    setSelectedSlot(slot);
  };

  const confirmBooking = async () => {
    try {
      const apptData = {
        patient_id: 1, // Mock patient for now
        doctor_id: parseInt(selectedDoctorId),
        appointment_datetime: new Date().toISOString().split('T')[0] + 'T' + selectedSlot.time + ':00',
        reason: "Consultation"
      };
      await api.post('/appointments/', apptData);
      alert("Appointment booked successfully!");
      fetchSchedule(selectedDoctorId);
      setSelectedSlot(null);
    } catch (error) {
      alert("Booking failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <div className="schedule-container">
      <div className="date-header">
        <select value={selectedDoctorId} onChange={e => setSelectedDoctorId(e.target.value)} className="form-input" style={{ width: 'auto' }}>
          <option value="">Select Doctor</option>
          {doctors.map(d => <option key={d.id} value={d.id}>{d.full_name} ({d.specialization})</option>)}
        </select>
      </div>
      {loading ? <div>Loading schedule...</div> : (
        <div className="slots-grid">
          {slots.map((slot) => (
            <div key={slot.time} className={`time-slot slot-${slot.status}`} onClick={() => handleSlotClick(slot)}>
              <span className="time-label">{slot.time}</span>
              <span className="slot-status">{slot.status}</span>
            </div>
          ))}
        </div>
      )}
      {selectedSlot && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Book {selectedSlot.time}</h3>
            <p>Confirm appointment with Dr. {doctors.find(d => d.id == selectedDoctorId)?.full_name}?</p>
            <button className="btn-primary" onClick={confirmBooking}>Confirm</button>
            <button className="btn-sm" onClick={() => setSelectedSlot(null)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DoctorSchedule;