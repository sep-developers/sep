/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
*
* This file is part of SEP
*
* Copyright 1993-2011 Emmanuel Bertin -- IAP/CNRS/UPMC
* Copyright 2014 SEP developers
*
* SEP is free software: you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* SEP is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public License
* along with SEP.  If not, see <http://www.gnu.org/licenses/>.
*
*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

#define	UNKNOWN	        -1    /* flag for LUTZ */
#define	CLEAN_ZONE      10.0  /* zone (in sigma) to consider for processing */
#define CLEAN_STACKSIZE 3000  /* replaces prefs.clean_stacksize  */
                              /* (MEMORY_OBJSTACK in sextractor inputs) */
#define CLEAN_MARGIN    0  /* replaces prefs.cleanmargin which was set based */
                           /* on stuff like apertures and vignet size */
#define	MARGIN_SCALE   2.0 /* Margin / object height */
#define	MARGIN_OFFSET  4.0 /* Margin offset (pixels) */
#define	MAXDEBAREA     3   /* max. area for deblending (must be >= 1)*/
#define	MAXPICSIZE     1048576 /* max. image size in any dimension */

/* plist-related macros */
#define	PLIST(ptr, elem)	(((pbliststruct *)(ptr))->elem)
#define	PLISTEXIST(elem)	(plistexist_##elem)
#define	PLISTPIX(ptr, elem)	(*((PIXTYPE *)((ptr)+plistoff_##elem)))

/* Extraction status */
typedef	enum {COMPLETE, INCOMPLETE, NONOBJECT, OBJECT} pixstatus;

/* Temporary object parameters during extraction */
typedef struct structinfo
{
  int64_t	pixnb;	    /* Number of pixels included */
  int64_t	firstpix;   /* Pointer to first pixel of pixlist */
  int64_t	lastpix;    /* Pointer to last pixel of pixlist */
  short	flag;	    /* Extraction flag */
} infostruct;

typedef	char pliststruct;      /* Dummy type for plist */

typedef struct
{
  int64_t     nextpix;
  int64_t     x, y;
  PIXTYPE value;
} pbliststruct;

/* array buffer struct */
typedef struct
{
  const BYTE *dptr;         /* pointer to original data, can be any supported type */
  int dtype;          /* data type of original data */
  int64_t dw, dh;         /* original data width, height */
  PIXTYPE *bptr;      /* buffer pointer (self-managed memory) */
  int64_t bw, bh;         /* buffer width, height (bufw can be larger than w due */
                      /* to padding). */
  PIXTYPE *midline;   /* "middle" line in buffer (at index bh/2) */
  PIXTYPE *lastline;  /* last line in buffer */
  array_converter readline;  /* function to read a data line into buffer */
  int64_t elsize;         /* size in bytes of one element in original data */
  int64_t yoff;           /* line index in original data corresponding to bufptr */
} arraybuffer;


/* globals */
extern _Thread_local int64_t plistexist_cdvalue, plistexist_thresh, plistexist_var;
extern _Thread_local int64_t plistoff_value, plistoff_cdvalue, plistoff_thresh, plistoff_var;
extern _Thread_local int64_t plistsize;
extern _Thread_local unsigned int randseed;

typedef struct
{
  /* thresholds */
  float	   thresh;		             /* detect threshold (ADU) */
  float	   mthresh;		             /* max. threshold (ADU) */

  /* # pixels */
  int64_t	   fdnpix;		       	/* nb of extracted pix */
  int64_t	   dnpix;	       		/* nb of pix above thresh  */
  int64_t	   npix;       			/* "" in measured frame */
  int64_t	   nzdwpix;			/* nb of zero-dweights around */
  int64_t	   nzwpix;		       	/* nb of zero-weights inside */

  /* position */
  int64_t	   xpeak, ypeak;                     /* pos of brightest pix */
  int64_t	   xcpeak,ycpeak;                    /* pos of brightest pix */
  double   mx, my;        	             /* barycenter */
  int64_t	   xmin,xmax,ymin,ymax,ycmin,ycmax;  /* x,y limits */

  /* shape */
  double   mx2,my2,mxy;			     /* variances and covariance */
  float	   a, b, theta, abcor;		     /* moments and angle */
  float	   cxx,cyy,cxy;			     /* ellipse parameters */
  double   errx2, erry2, errxy;      /* Uncertainties on the variances */

  /* flux */
  float	   fdflux;	       		/* integrated ext. flux */
  float	   dflux;      			/* integrated det. flux */
  float	   flux;       			/* integrated mes. flux */
  float	   fluxerr;			/* integrated variance */
  PIXTYPE  fdpeak;	       		/* peak intensity (ADU) */
  PIXTYPE  dpeak;      			/* peak intensity (ADU) */
  PIXTYPE  peak;       			/* peak intensity (ADU) */

  /* flags */
  short	   flag;			     /* extraction flags */

  /* accessing individual pixels in plist*/
  int64_t	   firstpix;			     /* ptr to first pixel */
  int64_t	   lastpix;			     /* ptr to last pixel */
} objstruct;

typedef struct
{
  int64_t           nobj;	  /* number of objects in list */
  objstruct     *obj;	  /* pointer to the object array */
  int64_t           npix;	  /* number of pixels in pixel-list */
  pliststruct   *plist;	  /* pointer to the pixel-list */
  PIXTYPE       thresh;   /* detection threshold */
} objliststruct;


int analysemthresh(int objnb, objliststruct *objlist, int minarea,
		   PIXTYPE thresh);
void preanalyse(int, objliststruct *);
void analyse(int, objliststruct *, int, double);

typedef struct {
	infostruct  *info, *store;
	char	   *marker;
	pixstatus   *psstack;
	int64_t         *start, *end, *discan;
	int64_t         xmin, ymin, xmax, ymax;
} lutzbuffers;

int  lutzalloc(int64_t, int64_t, lutzbuffers *);
void lutzfree(lutzbuffers *);
int  lutz(pliststruct *plistin,
	  int64_t *objrootsubmap, int64_t subx, int64_t suby, int64_t subw,
	  objstruct *objparent, objliststruct *objlist, int minarea,
	  lutzbuffers *buffers);

void update(infostruct *, infostruct *, pliststruct *);

typedef struct {
	objliststruct *objlist;
	short *son, *ok;
	lutzbuffers lutz;
} deblendctx;

int  allocdeblend(int deblend_nthresh, int64_t w, int64_t h, deblendctx *);
void freedeblend(deblendctx *);
int  deblend(objliststruct *, objliststruct *, int, double, int, deblendctx *);

/*int addobjshallow(objstruct *, objliststruct *);
int rmobjshallow(int, objliststruct *);
void mergeobjshallow(objstruct *, objstruct *);
*/
int addobjdeep(int, objliststruct *, objliststruct *);

int convolve(arraybuffer *buf, int64_t y, const float *conv, int64_t convw, int64_t convh,
             PIXTYPE *out);
int matched_filter(arraybuffer *imbuf, arraybuffer *nbuf, int64_t y,
                   const float *conv, int64_t convw, int64_t convh,
                   PIXTYPE *work, PIXTYPE *out, int noise_type);
