/* eslint-disable react/jsx-no-duplicate-props */
import React, { useContext, useRef, useState } from 'react';
import { useDetectClickOutside } from 'react-detect-click-outside';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import AuthContext from './AuthContext';

export default function Card({ card }) {
	const { authTokens } = useContext(AuthContext);
	const [open, setOpen] = useState(false);
	const [title, setTitle] = useState(card.title);
	const titleInput = useRef();
	const openButton = useRef();

	const getCard = async () => {
		const response = await
		fetch(`api/cards/${card.id}`, {
			method: 'GET',
			headers: { Authorization: `Bearer ${String(authTokens.access)}` },
		});
		const data = await response.json();
		return data;
	};

	const handleOpen = async () => {
		await setOpen(true);
		const inputElement = titleInput.current.querySelector('textarea');
		inputElement.focus();
		inputElement.select();
	};

	const handleClose = async () => {
		if (title !== card.title) {
			const newCard = await getCard();
			setTitle(newCard.title);
		}
		setOpen(false);
	};

	const handleChange = (e) => {
		if (!e.target.value.includes('\n')) {
			setTitle(e.target.value);
		}
	};

	const updateTitle = async () => {
		if (title.trim()) {
			await fetch(`api/cards/${card.id}`, {
				method: 'PATCH',
				headers: {
					Authorization: `Bearer ${String(authTokens.access)}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ title }),
			});
		}
		handleClose();
	};

	const handleKeyUp = (e) => {
		if (e.key === 'Escape') {
			handleClose();
		} else if (e.key === 'Enter') {
			updateTitle();
		}
	};

	const inputWrapper = useDetectClickOutside({
		disableKeys: true,
		onTriggered: (e) => {
			if (open && !openButton.current.contains(e.target)) {
				handleClose();
			}
		},
	});

	return (
		<div>
			<Button
				disableRipple
				color="inherit"
				component={Paper}
				elevation={2}
				onClick={handleOpen}
				ref={openButton}
				sx={{
					backgroundColor: 'grey.900',
					display: open ? 'none' : 'block',
					fontSize: '1rem',
					fontWeight: 400,
					justifyContent: 'start',
					lineHeight: 1.5,
					mb: 1,
					mx: 1,
					p: 1,
					textTransform: 'none',
					wordBreak: 'break-word',
				}}
			>
				{title}
			</Button>

			<Paper
				elevation={0}
				ref={inputWrapper}
				sx={{
					backgroundColor: 'grey.900',
					display: open ? 'block' : 'none',
					mb: 1,
					px: 1,
				}}
			>
				<TextField
					fullWidth
					multiline
					InputProps={{ sx: { p: 0 } }}
					onChange={handleChange}
					onKeyUp={handleKeyUp}
					ref={titleInput}
					size="small"
					sx={{ backgroundColor: 'grey.900' }}
					value={title}
					variant="filled"
					inputProps={{
						maxLength: 128,
						sx: {
							letterSpacing: '0.02857em',
							lineHeight: 1.5,
							p: 1,
						},
					}}
				/>
				<Box
					sx={{
						alignItems: 'center',
						display: 'flex',
						gap: 1,
						mt: 1,
					}}
				>
					<Button
						onClick={updateTitle}
						size="small"
						variant="contained"
					>
						Save
					</Button>
				</Box>
			</Paper>
		</div>
	);
}