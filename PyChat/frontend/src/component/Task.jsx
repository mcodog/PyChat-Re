import React, { useEffect, useState, useContext } from 'react'
import Divider from '@mui/material/Divider'
import axiosInstance from '../utils/AxiosInstace'
import { AuthContext } from '../utils/AuthContext';
import Badge from '@mui/material/Badge';
// import AddChart from '@mui/icons-material/Mail';
import ArticleIcon from '@mui/icons-material/Article';

const Task = () => {
  const { isAuthenticated, userId, user, loading } = useContext(AuthContext);
  const [tasks, setTasks] = useState()
  const retrieveTasks = async () => {
    try {
      const res = await axiosInstance.get('/tasks')
      const filteredChats = res.data.filter(task => task.user == user);
      setTasks(filteredChats);
      console.log(res)
    } catch (e) {
      console.log(e)
    }
  }

  useEffect(() => {
    retrieveTasks()
  }, [])
  return (
    <div className='dashboard-content__container'>
      <div className="dashboard-title__common">
        Tasks
      </div>
      <Divider />
      <div className="sm-spacer"></div>
      <div className="tiles-container">
        {
          tasks ? (
            tasks.map((task) => {
              return (
                <div className="item-tile">
                  <div className="title">
                    <Badge
                      badgeContent={task.id}
                      sx={{
                        "& .MuiBadge-badge": {
                          backgroundColor: "#ff495b",
                          color: "white", // Optional: change the text color inside the badge
                        },
                      }}
                    >
                      <ArticleIcon color="#ff495b" />
                    </Badge> &nbsp;
                    {task.title || 'Untitled'}</div>
                  <div className="sm-spacer"></div>
                  <Divider />
                  <div className="sm-spacer"></div>
                  <div className="status">Status: <span className='colored'>{task.status}</span></div>
                  <div className="tile-controls">
                    <button>Set Complete</button>
                    <button>Delete</button>
                  </div>
                </div>
              )
            })
          ) : (
            null
          )
        }
      </div>
    </div>
  )
}

export default Task