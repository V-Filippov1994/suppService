import React, {useState} from "react";
import axios from 'axios';
import {api} from "../../api";
import {FABRICS} from "../../api/urls";


const FabricForm = () => {
    const [fabricName, setFabricName] = useState('');
    const [success, setSuccess] = useState('');
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        setError(null);
        setFabricName('');
        setSuccess('');

        e.preventDefault();
        if (fabricName) {
            const formData = {'name': fabricName}
            const response = await api('post', FABRICS, formData);
            if (response.data.error) {
                setError(response.data.error);
            } else {
                setSuccess('Фабрика успешно добавлена')
            }
        }
        else {
            setError('Заполните поле');
        }
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>Название фабрики:</label>
                <input type="text"
                       id="fabric_name"
                       placeholder="Ф1"
                       value={fabricName}
                       style={{width: '97%'}}
                       onChange={(e) => setFabricName(e.target.value)}/>
                <button className="btn-primary">Сохранить</button>
            </form>
            {success && (
                <div style={{
                      color: '#1a5d1a',
                      marginTop: '15px',
                    }}>
                    {success}
                </div>
            )}
            {error && (
              <div
                className="error-message"
                style={{
                  color: '#e74c3c',
                  marginTop: '15px',
                }}
              >
                {error}
              </div>
            )}
        </div>
    )
}

export default FabricForm;